from flask import Flask, request, jsonify
from QueryParser import QueryParser
from QueryParser import WhereCondition
from typing import Dict, List

app = Flask(__name__)

class SQLGenerator:
    @staticmethod
    def build_select_clause(columns: List[str]) -> str:
        """Build the SELECT clause of the SQL query."""
        if not columns:
            return "SELECT *"
        
        # Mapping of natural language to SQL aggregate functions
        agg_functions = {
            'sum of': 'SUM',
            'avg of': 'AVG',
            'average of': 'AVG',
            'count of': 'COUNT',
            'max of': 'MAX',
            'min of': 'MIN'
        }
        
        processed_columns = []
        for col in columns:
            # Check for aggregate functions
            matched = False
            for prefix, sql_func in agg_functions.items():
                if col.lower().startswith(prefix):
                    column = col.lower().split()[-1]
                    processed_columns.append(f"{sql_func}({column}) AS {sql_func.lower()}_{column}")
                    matched = True
                    break
            
            # If no aggregate function matched, use the column as-is
            if not matched:
                processed_columns.append(col)
        
        return f"SELECT {', '.join(processed_columns)}"
    
    @staticmethod
    def build_where_clause(conditions: List[WhereCondition]) -> str:
        """Build the WHERE clause of the SQL query."""
        if not conditions:
            return ""
        
        # Mapping of natural language operators to SQL operators
        operator_mapping = {
            'equals': '=',
            'equal to': '=',
            'greater than': '>',
            'less than': '<',
            'greater than or equal to': '>=',
            'less than or equal to': '<=',
            'not equal to': '!='
        }
        
        processed_conditions = []
        for condition in conditions:
            # Split the condition into parts (field, operator, value)
            parts = condition.condition.lower().split()
            
            if len(parts) < 3:
                continue
                
            field = parts[0]
            value = parts[-1]
            
            # Extract the operator phrase by joining the middle terms
            operator_phrase = ' '.join(parts[1:-1])
            
            # Find the matching SQL operator
            sql_operator = None
            for nl_operator, sql_op in operator_mapping.items():
                if nl_operator in operator_phrase:
                    sql_operator = sql_op
                    break
            
            if not sql_operator:
                continue
                
            # Add quotes for string values (if value is alphabetic)
            if value.isalpha():
                value = f"'{value}'"
            
            # Construct the SQL condition
            processed_condition = f"{field} {sql_operator} {value}"
            processed_conditions.append(processed_condition)
            
            # Add the connecting operator (AND/OR) if present
            if condition.operator:
                processed_conditions.append(condition.operator)
        
        # Join all parts with spaces
        where_clause = " ".join(processed_conditions)
        return f"WHERE {where_clause}" if where_clause else ""
    
    @staticmethod
    def build_group_by_clause(columns: List[str]) -> str:
        """Build the GROUP BY clause of the SQL query."""
        if not columns:
            return ""
        return f"GROUP BY {', '.join(columns)}"
    
    @staticmethod
    def build_order_by_clause(columns: List[str], direction: str) -> str:
        """Build the ORDER BY clause of the SQL query."""
        if not columns:
            return ""
        return f"ORDER BY {', '.join(columns)} {direction}"
    
    @classmethod
    def generate_sql_query(cls, table_name: str, query_params: Dict) -> str:
        """Generate a complete SQL query from the parsed parameters."""
        clauses = [
            cls.build_select_clause(query_params['select']),
            f"FROM {table_name}",
            cls.build_where_clause(query_params['where']),
            cls.build_group_by_clause(query_params['group_by']),
            cls.build_order_by_clause(query_params['sort'], query_params['sort_direction'])
        ]
        
        # Filter out empty clauses and join with spaces
        sql_query = " ".join(clause for clause in clauses if clause)
        return sql_query

@app.route('/',methods=['GET'])
def home():
    return "Welcome"

@app.route('/generate-query', methods=['POST'])
def generate_query():
    try:
        data = request.get_json()
        
        if not data or 'table_name' not in data or 'query' not in data:
            return jsonify({
                'error': 'Missing required fields: table_name and query'
            }), 400
        
        table_name = data['table_name']
        query_string = data['query']
        
        # Parse the natural language query
        parser = QueryParser()
        query_params = parser.tokenize(query_string)
        
        # Generate SQL query
        sql_query = SQLGenerator.generate_sql_query(table_name, query_params)
        
        return jsonify({
            'sql_query': sql_query,
            # 'parsed_params': query_params
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
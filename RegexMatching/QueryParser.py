from enum import Enum
import re

class QueryType(Enum):
    SELECT = "Top|Bottom|show|find|select|get|display|list"
    GROUP_BY = "group by|grouped by"
    WHERE = "where|with|having|whose"
    SORT = "sort by|order by|sorted by|ordered by"

class WhereCondition:
    def __init__(self, condition, operator=None):
        self.condition = condition.strip()
        self.operator = operator

    def __str__(self):
        if self.operator:
            return f"{self.condition} {self.operator}"
        return self.condition
    
    def __repr__(self):
        return f"WhereCondition(condition='{self.condition}', operator={self.operator})"
    
class QueryParser:
    def __init__(self):
        """
        Initialize Query Params
        """
        self.query_params = {
            'select': [],
            'group_by': [],
            'where': [],
            'sort': [],
            'sort_direction': 'ASC'  # Default sort direction
        }

    def parse_where_conditions(self, where_clause):
        """
        Parse where clause into conditions and their connecting operators
        """
        if not where_clause:
            return []
        
        # Split on ' AND ' and ' OR ' while preserving the operators
        pattern = r'\s+(AND|OR)\s+'
        parts = re.split(pattern, where_clause, flags=re.IGNORECASE)
        
        conditions = []
        for i in range(0, len(parts), 2):
            condition = parts[i].strip()
            # Get the operator that follows this condition (if any)
            operator = parts[i + 1].upper() if i + 1 < len(parts) else None
            conditions.append(WhereCondition(condition, operator))
            
        return conditions
    
    def tokenize(self, query):
        """
        Tokenize the input query string into its component parts
        """

        # Convert to lowercase for easier matching
        patterns = {
            'select': re.compile(rf"(?:{QueryType.SELECT.value})\s+(.*?)\s+(?:{QueryType.GROUP_BY.value}|{QueryType.WHERE.value}|{QueryType.SORT.value}$)", re.IGNORECASE),
            'group_by': re.compile(rf"(?:{QueryType.GROUP_BY.value})\s+(.*?)(?:\s+{QueryType.WHERE.value}|\s+{QueryType.SORT.value}|$)", re.IGNORECASE),
            'where': re.compile(rf"(?:{QueryType.WHERE.value})\s+(.*?)(?:\s+{QueryType.GROUP_BY.value}|\s+{QueryType.SORT.value}|$)", re.IGNORECASE),
            'sort': re.compile(rf"(?:{QueryType.SORT.value})\s+(\S+)(?:\s+(asc|desc))?", re.IGNORECASE),
        }

        # Extract SELECT part
        match = patterns['select'].search(query)
        if match:
            self.query_params['select'] = [col.strip() for col in match.group(1).split(",")]

        # Extract 'group_by'
        match = patterns['group_by'].search(query)
        if match:
            self.query_params['group_by'] = [col.strip() for col in match.group(1).split(",")]

        # Extract 'where'
        match = patterns['where'].search(query)
        if match:
            self.query_params['where'] = self.parse_where_conditions(match.group(1))

        # Extract 'sort'
        match = patterns['sort'].search(query)
        if match:
            self.query_params['sort'] = [col.strip() for col in match.group(1).split(",")]
            if match.group(2):
                self.query_params['sort_direction'] = match.group(2).upper()

        return self.query_params.copy()

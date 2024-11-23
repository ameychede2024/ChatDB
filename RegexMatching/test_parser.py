from QueryParser import QueryParser

def test_query_parser():
    parser = QueryParser()
    parser.tokenize("Show sales,amount grouped by product,category where amount is greater than 5 sorted by amount desc")
    print(parser.query_params)

    parser = QueryParser()
    parser.tokenize("List sales,amount with amount is greater than 5 grouped by product,category sorted by sum of sales asc")
    print(parser.query_params)

    parser = QueryParser()
    parser.tokenize("Display sum of sales,amount grouped by product,category where amount is greater than 5 and city equals pune sorted by amount desc")
    print(parser.query_params["where"])

    parser = QueryParser()
    parser.tokenize("Select sales,amount where amount is greater than 5 or and city equals pune grouped by product,category sorted by amount")
    print(parser.query_params["where"])

if __name__ == "__main__":
    test_query_parser()

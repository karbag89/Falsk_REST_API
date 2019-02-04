class ErrorHandler:
    @staticmethod
    def checkIsCorrectUser(error):
        error_codes_dictionary = {400: "Request error", 404: "Resource with given ID does not exist",
                               405: "Page not found", 500: "Internal parameters is incorrect"}
        error_message = str(error)
        try:
            error_code = int(error_message[:error_message.find(" ")])
            for error_item in error_codes_dictionary.keys():
                if error_item == error_code:
                    return error_codes_dictionary[error_item]
        except:
            return error_message

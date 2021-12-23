class ReturnDictionaryKeys:
    CVC_success = 'success'
    CVC_debug_data = 'debug_data'
    CVC_return_msg = 'return_msg'


class ReturnCodes:
    CVC_success = True
    CVC_input_validation = 1001


class ErrorFunctions():

    @staticmethod
    def logException(function_name=None, action_description=None, exception_object=None, variables=None):
        variables_string = ''
        if type(function_name) != str:
            function_name = "Not Specified"
        if type(action_description) != str:
            action_description = "Not Specified"
        
        if variables != None:
            try:
                variables_string = ' . variables: {}.'.format(str(variables))
            except:
                variables_string = ' . Could not convert variables to strings.'
                
        try:
            e_msg = str(exception_object)
        except:
            e_msg = "could not convert exception to string" 
        
        output_string = 'expection occured in function: {}. while trying to: {}. exception: {} variables: {}'.format(function_name, action_description, e_msg, variables_string)
        return output_string 

    @staticmethod
    def parseException(action_description=None,exception_object=None,variables=None): 
        variables_string = ''
        e_msg = ''
        
        if type(action_description) != str:
            action_description = "Not Specified"
            
        if variables != None:
            try:
                variables_string = ' . variables: {}.'.format(str(variables))
            except:
                variables_string = ' . Could not convert variables to strings.'
                
        try:
            e_msg = str(exception_object)
        except:
            e_msg = "could not convert exception to string"
        
        output_string = 'expection occured while trying to: {}. exception: {} {}'.format(action_description, e_msg, variables_string)
        return output_string

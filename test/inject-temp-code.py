"""
inject temporary invite code
into production environment from envar
"""
import os
os.environ["APP_ENV"] = "prod"
from injection import *

def main():
    """
    execute inject invite code
    """
    tempcode = os.getenv("TEMP_INVITE_CODE")
    if tempcode is None:
        raise AttributeError("TEMP_INVITE_CODE is None")
    assert isinstance(tempcode, str), \
        f"expecting tempcode to be string, not {type(tempcode)}"
    inject_code = InjectInviteCode()
    inject_code.insert(code=tempcode)
    print('done')
    
if __name__ == '__main__':
    main()

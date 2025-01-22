from collector import Collector
from dotenv import load_dotenv
import asyncio
from okta.client import Client as OktaClient
import os

def meta():
    return {
        'plugin' : 'okta',
        'title'  : 'Okta',
        'link'  : 'https://github.com/okta/okta-sdk-python',
        'functions' : [ 'users'],
        'env' : {
            'OKTA_DOMAIN' : None,
            'OKTA_TOKEN' : None
        }
    }

async def users(client,C):
    data = []
    users, resp, err = await client.list_users()
    if err:
        C.lib.log("ERROR","src_okta",err)
        return False
    
    while True:
        for user in users:
            data.append({
                'id'               : user.id,
                'status'           : user.status,
                'created'          : user.created,
                'activated'        : user.activated,
                'status_changed'   : user.status_changed,
                'last_login'       : user.last_login,
                'last_updated'     : user.last_updated,
                'password_changed' : user.password_changed,
                'type' : {
                    'id' : user.type.id
                },
                'profile' : {
                    'login'                 : user.profile.login,
                    'first_name'            : user.profile.first_name,
                    'last_name'             : user.profile.last_name,
                    'nick_name'             : user.profile.nick_name,
                    'display_name'          : user.profile.display_name,
                    'email'                 : user.profile.email,
                    'secondEmail'           : user.profile.secondEmail,
                    'profile_url'           : user.profile.profile_url,
                    'preferred_language'    : user.profile.preferred_language,
                    'user_type'             : user.profile.user_type,
                    'organization'          : user.profile.organization,
                    'title'                 : user.profile.title,
                    'division'              : user.profile.division,
                    'department'            : user.profile.department,
                    'cost_center'           : user.profile.cost_center,
                    'employee_number'       : user.profile.employee_number,
                    'mobile_phone'          : user.profile.mobile_phone,
                    'primary_phone'         : user.profile.primary_phone,
                    'street_address'        : user.profile.street_address,
                    'city'                  : user.profile.city,
                    'state'                 : user.profile.state,
                    'zip_code'              : user.profile.zip_code,
                    'country_code'          : user.profile.country_code,
                }
            })
        if resp.has_next():
            users, err = await resp.next()
        else:
            break
    C.store('okta_users',data)

def main():
    C = Collector(meta())
    if C.test_environment():
        client = OktaClient({
            'orgUrl' : os.environ['OKTA_DOMAIN'],
            'token'  : os.environ['OKTA_TOKEN']
        })

        # == users
        loop = asyncio.get_event_loop()
        loop.run_until_complete(users(client,C))

if __name__ == '__main__':
    load_dotenv()
    main()
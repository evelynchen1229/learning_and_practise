from pytest import mark

import pandas as pd
import numpy as np
from test_utility import cell_value
from elis import email_update
from update import update
from moj_email import user_email, new_user_email_mapping

df_elis_2 = pd.read_csv('../file/elis/2020-8-25.csv')

@mark.cell_value
class CellValueTest:

    def test_cell_value_function_can_return_value(self):
        assert cell_value('GOODFELLOW-FARMER9712@476')
    
    def test_function_can_return_cell_value(self):
        expected = ['60da7e91-c3d5-44ca-a83a-3c7bf13465aa',
                'ca1d8575-70e2-4692-a907-a85cca891606',
                'ff446b83-4c0d-4b86-bfbb-b0b683030e8e'] 
 
        actual =  [cell_value('GANNER8194@476006'),cell_value('ZANG1834@476006'),cell_value('THOMAS7151@476006')]

        assert expected == actual

@mark.elis
class ElisTest:

    def test_elis_function_can_return_dataframe(self):
        assert str(type(email_update())) == "<class 'pandas.core.frame.DataFrame'>"
    
    def test_elis_have_the_latest_email_if_available(self):
        # first test case: id only exits in the latest elis user list
        # second test case: id only exists in both old and the latest user list
        # third test case: while initial test has three user lists, id only exists in the two old elis user lists but not the latest one
        # the emails from the two old elis user lists are different
        expected = ['HHJ.Jeremy.Gold.QC@ejudiciary.net',
                    'DJ.Geoff.Edwards@ejudiciary.net',
                    'laura.lisle@ejudiciary.net'] 
        
        actual = [cell_value('6f84981e-eba1-4b76-9329-20c59f9d6d84','id','userPrincipalName',email_update(email_update(df_latest=df_elis_2))),
                  cell_value('0f562e0e-0b42-45e7-98ce-8642d1390535','id','userPrincipalName',email_update(email_update(df_latest=df_elis_2))), 
                  cell_value('2c043e28-d8f2-4c27-8ba3-d9141f82ebaa','id','userPrincipalName',email_update(email_update(df_latest=df_elis_2)))
                  ]   

        assert expected == actual

@mark.update
class UpdateTest:
    
    def test_update_function_can_return_value(self):
        assert str(type(update())) == "<class 'pandas.core.frame.DataFrame'>"

    def test_update_function_can_return_the_latest_external_id(self):
        expected = ['8e76d634-9ab8-4bda-8029-f5cde195bb84','266c2c7a-7703-4bea-9949-598e6a99e975']

        actual = [cell_value('DEVANS@DCA','User Signon Identifier','External Id',update()),
                cell_value('HEILBRUNN0918@476006','User Signon Identifier','External Id',update())]

        assert expected == actual

    def test_update_function_can_return_the_latest_source(self):
        expected = ['elis','elis']

        actual = [cell_value('BOWEN0970@476006','User Signon Identifier','Data Source',update()),
                cell_value('MILLS7396@476006','User Signon Identifier','Data Source',update())]
        
        assert expected == actual

    def test_update_function_can_return_the_latest_email(self):
        expected = 'Recorder.Mills1@ejudiciary.net'
        actual = cell_value('MILLS7396@476006','User Signon Identifier','Email',update())
        assert expected == actual

    def test_update_function_has_no_duplicates(self):
        expected = [1]
        actual = update().groupby('User Signon Identifier')['Email'].transform('count').unique()
        assert np.array_equal(expected,actual)

@mark.email
class EmailTest:

    def test_user_email_function_can_return_value(self):
        assert user_email('000053@DCA')

    def test_user_email_function_can_skip_already_mapped_user(self):
        expected = ['000064@DCA',None,None]
        actual = [user_email('000064@DCA'),user_email('DEVANS@DCA'),user_email('FLAUX1905@476006')]
        assert expected == actual

    def test_new_email_mapping_fuction_returns_value(self): 
        assert str(type(new_user_email_mapping())) == "<class 'pandas.core.frame.DataFrame'>"

    # below test cases would need to get test case changed or delete the related test cases from user_email_for_report.csv
    @mark.skip
    def test_mapping_function_can_return_the_latest_email(self):
        # optional: checking all users have email mapped
        expected = ['EmploymentJudge.Cuthbert@ejudiciary.net','DDJMC.Natalie.Wortley@ejudiciary.net']
        actual = [cell_value('CUTHBERT2587@476006','User Signon Identifier','Email',new_user_email_mapping()),
                cell_value('WORTLEY4764@476006','User Signon Identifier','Email',new_user_email_mapping())
                ]
        assert expected == actual
    @mark.skip
    def test_mapping_function_can_return_the_latest_data_source(self):
        # optional: checking all users have email mapped
        expected = ['gdw','elis'] 

        actual = [cell_value('CUTHBERT2587@476006','User Signon Identifier','Data Source',new_user_email_mapping()),
                cell_value('WORTLEY4764@476006','User Signon Identifier','Data Source',new_user_email_mapping())
                ]

        assert expected == actual

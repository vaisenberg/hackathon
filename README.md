��#   h a c k a t h o n 
 
SpendemicCure - is an App which is not ready to its full application:
the idea behind is to help the User to control his/her assets  whilst assets are 
being defined as :bank account daily, Currency Assets and Stock Assets. We 
believe the End User is interested to optimise its assets, in order to do so we 
offer User to exercise the currency conversion presenting it as 3 portfolios in 
USD, EUR, CHF, taking into account that base currency at the moment is ILS. 
On top of that we are introducing an Option to get Portfolios of Shares in Apple,
Cisco, Oracle and EL AL.
The following as stated below , are the main functions of the App:
1. Creating a wallet for new user:
Using the menu created in Python and opening connection to PG admin
Using Faker to create test users and uploading them to PG Admin
2. Identifying end user by his unique code
3. Taking his new daily balance as cash at bank – we do not operate with his
banks account
4. Comparing it to the last one and if the balance is greater than 500 , we 
offer him to differentiate his cash assets by converting into 3 target 
currencies
5. Providing the exchange rates by means of API in Fixer and creating a 
class Converter from ILS to Currencies
6. Updating his wallet data
7. If the balance in ISL is less than 0 we fetching all his portfolios 
suggesting to sell to cover the minus
 

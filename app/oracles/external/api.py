import requests
import time

from .config import ADDRESS, API_ETHERSCAN, ALCHEMY, API_COINGECKO, API_LIQUIDITYFOLIO

class API():
    def __init__(self, _api_etherscan=API_ETHERSCAN, _alchemy=ALCHEMY):
        self.api_etherscan = _api_etherscan
        self.alchemy = _alchemy
    #
    def get(self, url, attempts=0):
        print("_"*100)
        print(url)
        response = requests.get(url)
        resp = response.json()

        if not bool(resp['status']) or resp['status'] == "0":
            if attempts > 4:
                return None
            print("\tStatus:\t{}".format(resp['status']))
            print("\tMessage:\t{}".format(resp['message']))
            print("\tResult:\t{}".format(resp['result']))
            if resp['result'] == "Max rate limit reached":
                print("Pausing 5 secs. Rate limit. Attempt: {}".format(attempts))
                time.sleep(5.5)
                return self.get(url, attempts + 1)
            elif resp['result'] == "Contract source code not verified":
                print("\nNot Verified: Proceed")
                return False
            else:
                print("Pausing 60 secs. Attempt: {}".format(attempts))
                time.sleep(61)
                return self.get(url, attempts + 1)
        return resp['result']
    #
    def post(self, url, my_obj, attempts=0):
        print("_"*100)
        print(url)
        response = requests.post(url, data = my_obj)
        resp = response.json()

        if not bool(resp['status']) or resp['status'] == "0":
            if attempts > 4:
                return None
            print("\tStatus:\t{}".format(resp['status']))
            print("\tMessage:\t{}".format(resp['message']))
            print("\tResult:\t{}".format(resp['result']))
            if resp['result'] == "Max rate limit reached":
                print("Pausing 5 secs. Rate limit. Attempt: {}".format(attempts))
                time.sleep(5.5)
                return self.get(url, my_obj, attempts + 1)
            elif resp['result'] == "Contract source code not verified":
                print("\nNot Verified: Proceed")
                return False
            else:
                print("Pausing 60 secs. Attempt: {}".format(attempts))
                time.sleep(61)
                return self.get(url, my_obj, attempts + 1)
        return resp['result']
    #
    # Etherescan
    # All transactions
    def get_txn_history(self, address=ADDRESS):
        url_start = "https://api.etherscan.io/api?module=account&action=txlist&address="
        url_end = "&sort=asc"
        url = url_start + address + url_end
        return self.get(url)
    #
    # ERC20 token transfer funcs
    def get_token_transfer(self, address=ADDRESS):
        url_start = "https://api.etherscan.io/api?module=account&action=tokentx&address="
        url_end = "&startblock=0&endblock=999999999&sort=asc&apikey="
        url = url_start + address + url_end + self.api_etherscan
        return self.get(url)
    #
    # Get contract ABI
    def get_contract_abi(self, address=ADDRESS):
        url_start = "https://api.etherscan.io/api?module=contract&action=getabi&address="
        url_end = "&apikey="
        url = url_start + address + url_end + self.api_etherscan
        return self.get(url)
    #
    # def get_transaction_receipt(self, address=ADDRESS, hash):
    #     url_start = "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&"
    #     tx_hash = "txhash=" + str(hash)
    #     api = "&apikey=" + self.api_etherscan
    #     url = url_start + tx_hash + api
    #     return self.get(url)
    def get_tokens_transfered(self, address=ADDRESS):
        url_start = "http://api.etherscan.io/api?module=account&action=tokentx&address="
        url_end = "&startblock=0&endblock=999999999&sort=asc&apikey="
        url = url_start + address + url_end + self.api_etherscan
        return self.get(url)

        #     {
        # "status": "1",
        # "message": "OK",
        # "result": [        {
        #     "blockNumber": "5291308",
        #     "timeStamp": "1521579199",
        #     "hash": "0x01b0d06eb882873be66dfc900117287a922fc8336aecd0269cb21e991ec771ef",
        #     "nonce": "46",
        #     "blockHash": "0x58deca23f23617523acc1022d6fa63b88db436b405741aeeac61dd54ec771078",
        #     "from": "0x17e33637f6b64e9082ea499481b6e6ebae7eea23",
        #     "contractAddress": "0xf53ad2c6851052a81b42133467480961b2321c09",
        #     "to": "0x448a5065aebb8e423f0896e6c5d525c040f59af3",
        #     "value": "1778959821291690476",
        #     "tokenName": "Pooled Ether",
        #     "tokenSymbol": "PETH",
        #     "tokenDecimal": "18",
        #     "transactionIndex": "42",
        #     "gas": "74541",
        #     "gasPrice": "2000000000",
        #     "gasUsed": "34694",
        #     "cumulativeGasUsed": "2236522",
        #     "input": "deprecated",
        #     "confirmations": "7100828"
        # },

    def get_transaction_receipt(self, contractAddress, address=ADDRESS):
        url = self.alchemy
        payload = {
          "jsonrpc": "2.0",
          "id": 0,
          "method": "alchemy_getAssetTransfers",
          "params": [
            {
              "fromBlock": "0xA97AB8",
              "toBlock": "0xA97CAC",
              "fromAddress": address,
              "contractAddresses": [
                contractAddress
              ],
              "maxCount": "0x5",
              "excludeZeroValue": True,
              "category": [
                "external",
                "token"
              ]
            }
          ]
        }
        return self.post(url, payload)
        # https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x4c73fd53daf9d5d1aa538552c605204ab163f12bac72cf09888e58ac27cd6dc8&apikey=E9V2IBKAHGCREJJ3RYAC5FRHSDI8MPDB5P
    #
    def get_token_historic(self, token_name, date):
        # date format = day-month-year
        url_start = "https://pro-api.coingecko.com/api/v3/coins/"
        url_end = "/history?date="
        api_prefix = "&x_cg_pro_api_key="
        url = url_start + token_name + url_end + date + api_prefix + API_COINGECKO
        return self.get(url)

    def get_token_historic(self, token_name, date):
        # date format = day-month-year
        url_start = "https://pro-api.coingecko.com/api/v3/coins/"
        url_end = "/history?date="
        api_prefix = "&x_cg_pro_api_key="
        url = url_start + token_name + url_end + date + api_prefix + API_COINGECKO
        return self.get(url)
        # 0xFAE2809935233d4BfE8a56c2355c4A2e7d1fFf1A
        #  Response =
        # {"id":"ethereum","symbol":"eth","name":"Ethereum","localization":{"en":"Ethereum","de":"Ethereum","es":"Ethereum","fr":"Ethereum","it":"Ethereum","pl":"Ethereum","ro":"Ethereum","hu":"Ethereum","nl":"Ethereum","pt":"Ethereum","sv":"Ethereum","vi":"Ethereum","tr":"Ethereum","ru":"эфириум","ja":"イーサリアム","zh":"以太坊","zh-tw":"以太幣","ko":"이더리움","ar":"يثريوم","th":"Ethereum","id":"Ethereum"},"image":{"thumb":"https://assets.coingecko.com/coins/images/279/thumb/ethereum.png?1595348880","small":"https://assets.coingecko.com/coins/images/279/small/ethereum.png?1595348880"},"market_data":{"current_price":{"aed":2850.371539644462,"ars":14428.426062422588,"aud":995.194970427022,"bch":0.3197733410710426,"bdt":64115.87649235829,"bhd":291.9684050028884,"bmd":776.080330355968,"brl":2570.69236667276,"btc":0.0550661260590115,"cad":974.252442712366,"chf":756.131185464168,"clp":476117.5218700828,"cny":5060.04375392092,"czk":16510.93441024889,"dkk":4809.79277099599,"eth":null,"eur":646.072905575396,"gbp":574.242790599303,"hkd":6063.94246525291,"huf":200624.5262003213,"idr":10526324.5845178,"ils":2697.461208234756,"inr":49576.0115031394,"jpy":87498.5947857359,"krw":827387.000995803,"kwd":233.84930122319065,"lkr":118848.94179071294,"ltc":3.3674962696346378,"mmk":1048948.7573864432,"mxn":15259.7571036573,"myr":3151.97265370773,"ngn":278239.72944209026,"nok":6361.561511141083,"nzd":1095.33261545286,"php":38741.93009137,"pkr":85691.51036242991,"pln":2699.78944922583,"rub":44831.9876597394,"sar":2910.8444950661296,"sek":6345.38566881549,"sgd":1037.79013935861,"thb":25276.93635969388,"try":2943.0471722939196,"twd":23078.3007837955,"uah":21818.075156632167,"usd":776.080330355968,"vef":7749.17917237161,"vnd":17617709.448545583,"xag":45.5982816171296,"xau":0.593887712001601,"xdr":544.948862449685,"zar":9624.70767217234,"bits":55066.1260590115,"link":1033.350503664953,"sats":5506612.60590115},"market_cap":{"aed":275666412158.91644,"ars":1395408419712.3152,"aud":96247742822.4799,"bch":30926062.939892814,"bdt":6200803435357.499,"bhd":28236979478.453182,"bmd":75056629369.4547,"brl":248617954406.529,"btc":5325579.90810972,"cad":94222339678.9451,"chf":73127298711.5129,"clp":46046491551866.766,"cny":489369223488.846,"czk":1596812902093.5408,"dkk":465166838065.518,"eth":null,"eur":62483292930.7423,"gbp":55536426599.4528,"hkd":586458726409.706,"huf":19402889258297.734,"idr":1018026629537628,"ils":260878079530.88217,"inr":4794617484120.78,"jpy":8462203385787.15,"krw":80018623137069.5,"kwd":22616138618.23346,"lkr":11494172221638.291,"ltc":325678811.2347301,"mmk":101446403202349.73,"mxn":1475808480639.84,"myr":304834994521.104,"ngn":26909245643441.95,"nok":615242193206.5948,"nzd":105932299710.021,"php":3746826938123.19,"pkr":8287435825659.473,"pln":261103249418.991,"rub":4335811320111.18,"sar":281514899776.01373,"sek":613677787880.649,"sgd":100367225925.422,"thb":2444594418563.1396,"try":284629299555.0699,"twd":2231958987559.48,"uah":2110079480863.955,"usd":75056629369.4547,"vef":749442095499.8513,"vnd":1703851826539282.5,"xag":4409921485.38428,"xau":57436335.0586816,"xdr":52703339067.2732,"zar":930829049884.876,"bits":5325579908109.72,"link":99937857884.82108,"sats":532557990810972.0},"total_volume":{"aed":4046034846.0402226,"ars":20480808838.47108,"aud":1412655674.16308,"bch":453910.6789459186,"bdt":91010967119.34288,"bhd":414442231.1807888,"bmd":1101627635.65143,"brl":3649036888.46997,"btc":78165.0608604499,"cad":1382928252.41502,"chf":1073310297.27701,"clp":675837538195.7958,"cny":7182612184.44733,"czk":23436880082.26615,"dkk":6827386845.19335,"eth":null,"eur":917085177.382371,"gbp":815124031.564658,"hkd":8607622612.54426,"huf":284781760092.25116,"idr":14941868271320.7,"ils":3828982254.6154575,"inr":70371973365.4134,"jpy":124202181560.794,"krw":1174456238644.35,"kwd":331943540.8021245,"lkr":168703256123.65997,"ltc":4780081.144281872,"mmk":1488957900774.41,"mxn":21660863548.7598,"myr":4474150479.43472,"ngn":394954701595.11993,"nok":9030085794.540195,"nzd":1554798687.99118,"php":54993251571.7194,"pkr":121637068050.24263,"pln":3832287137.52241,"rub":63637943954.2033,"sar":4131874773.0378184,"sek":9007124569.73032,"sgd":1473118506.94581,"thb":35880012093.16707,"try":4177585710.1515384,"twd":32759101001.3665,"uah":30970240591.256165,"usd":1101627635.65143,"vef":10999776177.787512,"vnd":25007921018296.016,"xag":64725680.0653692,"xau":843009.531905899,"xdr":773541994.829357,"zar":13662044432.782,"bits":78165060860.4499,"link":1466816549.299084,"sats":7816506086044.99}},"community_data":{"facebook_likes":null,"twitter_followers":268932,"reddit_average_posts_48h":1.723,"reddit_average_comments_48h":49.383,"reddit_subscribers":238835,"reddit_accounts_active_48h":"5626.0"},"developer_data":{"forks":3322,"stars":10872,"subscribers":1195,"total_issues":2823,"closed_issues":2158,"pull_requests_merged":1201,"pull_request_contributors":179,"code_additions_deletions_4_weeks":{"additions":null,"deletions":null},"commit_count_4_weeks":null},"public_interest_stats":{"alexa_rank":8311,"bing_matches":null}}

    #
    # https://www.liquidityfolio.com/app/fb72383c1a8b4f8e9718b835cd93b603/api
    def liquidityfolio_analysis_request(self, address):
        url = "https://api.liquidityfolio.com/run_analysis"
        payload = {
            "api_key": API_LIQUIDITYFOLIO,
            "address": address
        }
        return self.post(url, payload)

    def liquidityfolio_analysis_retrieve(self, request_id):
        url = "https://api.liquidityfolio.com/retrieve_analysis"
        payload = {
            "api_key": API_LIQUIDITYFOLIO,
            "request_id": address
        }
        return self.post(url, payload)

    def liquidityfolio_all_pools_returns(self, request_id):
        url = "https://api.liquidityfolio.com/all_pools_returns"
        payload = {
            "api_key": API_LIQUIDITYFOLIO,
            "request_id": address
        }
        return self.post(url, payload)


#     def get_event_log(self, address=ADDRESS):
#         url_start = "https://api.etherscan.io//api?module=logs&action=getLogs&address="
#         /api?module=logs&action=getLogs
#
#
# &fromBlock=379224
# &toBlock=latest
# &address=0x17e33637f6B64E9082Ea499481b6e6EbAE7EEA23
# &topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545
# &apikey=E9V2IBKAHGCREJJ3RYAC5FRHSDI8MPDB5P
#     #
    # Coingecko

import unittest
from wta_hikes.wta_scrapers.wta_scrapers.spiders.hikes_scraper import WtaHikeScraper
from wta_hikes.wta_scrapers.test.responses import fake_response_from_file

class IcodropsUpcomingSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = WtaHikeScraper()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('data/hike_landing.html'))

        actual_urls = sorted([str(x.url) for x in results])
        print(actual_urls)
        #print(actual_urls)
        # self.assertEqual(actual_urls, expected_urls)

    def test_gonetwork(self):
        expected = {'AmountRaised': '$28,302,290',
                    'Bitcointalk': 'https://bitcointalk.org/index.php?topic=2352537.0;all',
                    'CurrencyAccepted': ' ETH, BTC',
                    'Description': 'A highly scalable, low cost mobile first network '
                                   'infrastructure for Ethereum.',
                    'FloatAmount': ['100,000,000'],
                    'Github': 'https://github.com/gonetwork-project',
                    'KYC_AML': " Yes (period isn't set)",
                    'Medium': 'https://medium.com/@gonetwork',
                    'Project': 'GoNetwork',
                    'Source': 'http://www.example.com',
                    'Telegram': 'https://t.me/joinchat/Geu7vA2LFdDv5RqxFYqCtw '
                                'https://t.me/gonetworkAnn',
                    'Ticker': 'GOT',
                    'Twitter': 'https://twitter.com/gonetwork_co',
                    'Website': 'https://gonetwork.co/?utm_source=icodrops',
                    'Whitelist': " Yes (period isn't set, JOIN\n)"}
        self.do_parse_profile_test('data/rachel_lake.html', expected)

    def do_parse_profile_test(self, response_path, expected, debug=False):
        actual = self.spider.parse_profiles(fake_response_from_file(response_path))
        if debug:
            print(actual)
        self.assertDictEqual(expected, dict(actual))

if __name__ == '__main__':
    unittest.main()
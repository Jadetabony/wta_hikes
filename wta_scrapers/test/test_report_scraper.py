import unittest
from wta_hikes.wta_scrapers.wta_scrapers.spiders.trip_report import TripReportScraper
from wta_hikes.wta_scrapers.test.responses import fake_response_from_file

class IcodropsUpcomingSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = TripReportScraper()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('data/trip_report_landing.html'))

        actual_urls = sorted([str(x.url) for x in results])
        print(actual_urls)
        #print(actual_urls)
        # self.assertEqual(actual_urls, expected_urls)

    def test_hike_scraper(self):
        expected = {'HikeName': 'Melakwa Lake',
                    'AuthorName': '',
                    'TrailConditions': 'Minor obstacles posing few problems',
                    'Road': 'Road suitable for all vehicles',
                    'Bugs': 'Bugs were not too bad',
                    'Snow': 'Snow free',
                    'ReportText': "We started hiking about 9:15 on Tuesday and had no difficulty"
                                  " parking in the main lot.  It was a warm humid day and where "
                                  "there was no tree coverage on the trail it was very hot.  "
                                  "No bugs at the parking lot or along the trail.  At the lake "
                                  "there were flies but no one saw mosquitoes.  Most of our "
                                  "group swam in the main lake and two of us swam in the small "
                                  "lake which was much, much colder.  The trail up to the lake"
                                  " past the falls is rocky so we didn't save much time on the"
                                  " descent.  This is a beautiful area!",
                    'DateHiked': 'Jul 31, 2018',
                    'Url': 'http://www.example.com'}
        self.do_parse_profile_test('data/trip_report.html', expected)

    def do_parse_profile_test(self, response_path, expected, debug=False):
        actual = self.spider.parse_profiles(fake_response_from_file(response_path))
        actual = dict(actual)
        if debug:
            print(actual)
        self.assertDictEqual(expected, dict(actual))

    # def do_parse_pages_test(self, response_path, debug=False):
    #     actual = self.spider.parse_pages(fake_response_from_file(response_path))
    #     if debug:
    #         print(actual)
    #     self.assertEqual(99, len(actual))


if __name__ == '__main__':
    unittest.main()
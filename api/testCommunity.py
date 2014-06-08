import settings
from core.runners import Trash
from core.decorators import authorize

class TestCommunity(Trash):
    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_one_create_community_fail(self):
        with self.assertRaises(Exception) as cm:
            self.post("communities", {})

        self.assertIn("required parameter", cm.exception.message)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_two_create_open_community_fail(self):
        print self.post("communities", {
            "title": "Community Open",
            "plan_type": "open"
        })


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_two_create_open_community_fail(self):
        print self.post("communities", {
            "title": "Community Open",
            "plan_type": "open",
            "plan_id": "140031151227562517735425"
        })

    #@authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    #def test_two_create_open_community(self):
    #    print self.post("communities", {
    #        "title": "Community Test1", "plan_type": "retail"})


    #@authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    #def test_two_create_open_community(self):
    #    print self.post("communities", {"title": "Community Test1", "plan_type": "retail"})


    #@authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    #def test_two(self):
    #    pass

if __name__ == '__main__':
    TestCommunity.go_run()

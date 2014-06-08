import settings
from core.runners import Trash
from core.decorators import authorize

class TestCommunity(Trash):
    community_id = None

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_1_create_community_fail(self):
        """
        Test should fail saying title is a required parameter.
        """
        with self.assertRaises(Exception) as cm:
            self.post("communities", {})

        self.assertIn("required parameter", cm.exception.message)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_2_create_open_community_fail(self):
        """
        User must be an administrator or BillPlan owner to create a community.
        """
        with self.assertRaises(Exception) as cm:
            community_id = self.post("communities", {
                "title": "Community Open",
                "plan_type": "open"
            })

        self.assertIn("must use", cm.exception.message)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_3_create_open_community(self):
        ret = self.post("communities", {
            "title": "Community Open",
            "plan_type": "open",
            "plan_id": "140031151227562517735425"
        })

        self.__class__.community_id = ret["created"]

    def test_4_get_community_fail(self):
        with self.assertRaises(Exception) as cm:
            community = self.get(
                "community",
                community_id=self.community_id)

        self.assertIn("enough permission", cm.exception.message)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_5_get_community(self):
        community = self.get("community", community_id=self.community_id)
        self.assertEqual(community["community"]["_id"], self.community_id)

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

import settings
from core.runners import Trash, CLI
from core.decorators import authorize

CLI.add_argument('--plan',
                 dest="plan_id",
                 required=True,
                 type=str,
                 help='BillPlanID to be used')


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
            "plan_id": self.cli_args.plan_id
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

if __name__ == '__main__':
    TestCommunity.go_run()

import settings
from core.runners import Trash, CLI
from core.decorators import authorize

CLI.add_argument('--plan',
                 dest="plan_id",
                 required=True,
                 type=str,
                 help='BillPlanID to be used')

CLI.add_argument('--siminar',
                 dest="siminar_id",
                 type=str,
                 help='Siminar to be used')

class TestCommunity(Trash):
    community_id = None

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test_11_create_open_community_fail(self):
        """
        User must be an administrator or BillPlan owner to create a community.
        """
        with self.assertRaises(Exception) as cm:
            community_id = self.post("communities", {
                "title": "Community Open",
                "plan_type": "open"
            })

        self.assertIn("administrator", cm.exception.message)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_12_create_community_fail(self):
        """
        Test should fail saying title is a required parameter.
        """
        with self.assertRaises(Exception) as cm:
            self.post("plan_communities", {}, plan_id=self.cli_args.plan_id)

        self.assertIn("required parameter", cm.exception.message)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_13_create_open_community(self):
        ret = self.post(
            "plan_communities",
            {"title": "Community Open", "plan_type": "open"},
            plan_id=self.cli_args.plan_id)

        self.__class__.community_id = ret["created"]


    def test_21_get_community(self):
        """Anonymous community view"""
        community = self.get("community", community_id=self.community_id)
        self.assertTrue(community["community"]["user_is_nobody"])


    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test_22_get_community(self):
        """Student Community View"""
        community = self.get("community", community_id=self.community_id)
        self.assertTrue(community["community"]["user_is_nobody"])


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_23_get_community(self):
        community = self.get("community", community_id=self.community_id)
        self.assertEqual(community["community"]["_id"], self.community_id)


    def test_31_get_plan_communities(self):
        """Anonymous cannot get Plan"""
        with self.assertRaises(Exception) as cm:
            ret = self.get("plan_communities", plan_id=self.cli_args.plan_id)

        self.assertIn("You must be", cm.exception.message)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test_32_get_plan_communities(self):
        """Should not show up in Open Communities"""
        ret = self.get("communities")
        communities = [x["_id"] for x in ret["communities"]]
        self.assertNotIn(self.community_id, communities)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_33_get_plan_communities(self):
        """Instructor can access his Plan and community should show up"""
        ret = self.get("plan_communities", plan_id=self.cli_args.plan_id)

        communities = [x["_id"] for x in ret["communities"]]
        self.assertIn(self.community_id, communities)


    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test_41_edit_community_fail(self):
        with self.assertRaises(Exception) as cm:
            community = self.put(
                "community",
                {"changed_data": {"plan_id": self.cli_args.plan_id}},
                community_id=self.community_id)

        self.assertIn("enough permissions", cm.exception.message)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_42_edit_community_fail(self):
        with self.assertRaises(Exception) as cm:
            community = self.put(
                "community",
                {"changed_data": {"plan_id": self.cli_args.plan_id}},
                community_id=self.community_id)

        self.assertIn("plan_id", cm.exception.message)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_43_edit_community(self):
        new_title = "Edited Community title"

        ret = self.put(
            "community",
            {"changed_data": {"title": new_title}},
            community_id=self.community_id)

        community = self.get("community", community_id=self.community_id)
        self.assertEqual(community["community"]["title"], new_title)


    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test_add_siminar_to_community(self):
        if not self.cli_args.siminar_id:
            self.logger.error("need --siminar to run")
            return

        siminar_id = self.cli_args.siminar_id
        self.post("siminar_communities",
                  {"community_id": self.community_id},
                  siminar_id=siminar_id)

        siminar = self.get("siminar", siminar_id=siminar_id)
        self.assertEqual(siminar["siminar"]["community_ids"], [self.community_id])



if __name__ == '__main__':
    TestCommunity.go_run()

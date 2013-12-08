import unittest
import settings
from core.runners import Reuse
from core.decorators import authorize
from simtools.timezone import system_now

class UserCount(Reuse):

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test11_create_step(self):
        ret = self.post(
            "steps",
            data={
                "title": "Step 1 on %s" % system_now().strftime("%c")
            },
            **{"siminar_id": self.storage["siminar_id"]})

        self.assertIsNotNone(ret)
        self.storage["step_id"] = ret

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test12_create_content(self):
        ret = self.post(
            "jontents",
            data={
                "title": "Jontent 1 on",
                "body": "Sample Body",
                "content_type": "action",
                "is_published": True,
                "step_id": self.storage["step_id"],
                "siminar_id": self.storage["siminar_id"]
            })

        self.assertIsNotNone(ret)
        self.storage["jontent_id"] = ret

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test13_user_signup(self):
        cart_ret = self.post(
            "cart" ,
            data={"item_id": self.storage["siminar_id"]})

        cart_ret.update({"finalize": 1})

        ret = self.put(
            "cart",
            data=cart_ret)

        self.assertEqual(self.storage["siminar_id"], ret.get("siminar_id"))
        self.assertTrue(ret.get("paid"))

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test14_count_before(self):
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})

        todo_count = siminar.get("step_dict").get(self.storage["step_id"])["count"]["todo_count"]

        self.storage["todo_count"] = todo_count

        self.storage["oldest_step"] = siminar.get("oldest_step")

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test15_step_visited(self):
        ret = self.put(
            "step",
            data= {"visited": True},
            **{"step_id": self.storage["step_id"]})

        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test16_mark_done(self):
        ret = self.post(
            "jaction",
            **{"object_id": self.storage["jontent_id"], "handle": "done"})

        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test17_get_siminar(self):
        siminar = self.get("agora_get", {"object_id": self.storage["siminar_id"]})

        todo_count = siminar.get("step_dict").get(self.storage["step_id"])["count"]["todo_count"]
        self.assertIsNone(siminar.get("oldest_step"))
        self.assertEqual(
            todo_count, self.storage["todo_count"] - 1
        )

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test18_instructor_forum_count_before(self):
        ret = self.get(
            "authtoken")

        forum_count = ret.get("user").get("unread_forum").get("siminar_id")
        if forum_count:
            self.storage["instructor_forum_count"] = forum_count
        else:
            self.storage["instructor_forum_count"] = 0

        feed_count = ret.get("user").get("unread_feed")
        self.storage["instructor_feed_count"] = 0
        for index, count_d in enumerate(feed_count):
            if count_d["_id"] != [self.storage["siminar_id"]]:
                continue

            self.storage["instructor_feed_count"] = count_d["count"]

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test19_student_forum_count_before(self):
        ret = self.get(
            "authtoken")

        forum_count = ret.get("user").get("unread_forum").get("siminar_id")
        if forum_count:
            self.storage["student_forum_count"] = forum_count
        else:
            self.storage["student_forum_count"] = 0

        feed_count = ret.get("user").get("unread_feed")
        self.storage["student_feed_count"] = 0
        for index, count_d in enumerate(feed_count):
            if count_d["_id"] != [self.storage["siminar_id"]]:
                continue

            self.storage["student_feed_count"] = count_d["count"]

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test20_student_content(self):
        ret = self.post(
            "jontents",
            data={
                "title": "Student 1 on",
                "body": "Sample Body",
                "content_type": "action",
                "is_published": True,
                "topic_id": self.storage["siminar_id"]
            })

        self.assertIsNotNone(ret)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test21_instructor_forumcount(self):
        ret = self.get(
            "authtoken")

        forum_count = ret.get("user").get("unread_forum").get(self.storage["siminar_id"])
        if not forum_count:
            self.assertRaises(Exception)

        self.assertEqual(forum_count, self.storage["instructor_forum_count"]+1)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test22_l1_student(self):
        ret = self.post(
            "jaction",
            data={
                "title": "L1 by Student",
                "text": "",
                "privacy": "public"
            },
            **{"object_id": self.storage["jontent_id"], "handle": "responses"})

        self.storage["response_id"] = ret
        self.assertIsNotNone(ret)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test23_instructor_feedcount(self):
        ret = self.get(
            "authtoken")

        feed_count = ret.get("user").get("unread_feed")
        for index, count_d in enumerate(feed_count):
            if count_d["_id"] != self.storage["siminar_id"]:
                continue

            new_feed_count = count_d["count"]

        self.assertEqual(new_feed_count, self.storage["instructor_feed_count"]+1)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test24_l2_instructor(self):
        ret = self.post(
            "jaction",
            data={
                "text": "L2 by Instructor",
                "privacy": "public"
            },
            **{"object_id": self.storage["response_id"], "handle": "comments"})

        self.storage["comment_id"] = ret
        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test25_student_feedcount(self):
        ret = self.get(
            "authtoken")

        feed_count = ret.get("user").get("unread_feed")
        for index, count_d in enumerate(feed_count):
            if count_d["_id"] != self.storage["siminar_id"]:
                continue

            new_feed_count = count_d["count"]

        self.assertEqual(new_feed_count, self.storage["student_feed_count"]+1)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test26_l3_student(self):
        ret = self.post(
            "jaction",
            data={
                "text": "L3 by Student1",
                "parent_id": self.storage["comment_id"],
                "privacy": "public"
            },
            **{"object_id": self.storage["comment_id"], "handle": "comments"})

        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT2_EMAIL, settings.STUDENT2_PASSWORD)
    def test27_l3_another_student(self):
        ret = self.post(
            "jaction",
            data={
                "text": "L3 by Student2",
                "parent_id": self.storage["comment_id"],
                "privacy": "public"
            },
            **{"object_id": self.storage["comment_id"], "handle": "comments"})

        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test28_l3_second_student(self):
        ret = self.post(
            "jaction",
            data={
                "text": "Another L3 by Student1",
                "parent_id": self.storage["comment_id"],
                "privacy": "public"
            },
            **{"object_id": self.storage["comment_id"], "handle": "comments"})

        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test29_private_response(self):
        ret = self.post(
            "jaction",
            data={
                "title": "Private L1 by Student1",
                "text": "",
                "privacy": "private"
            },
            **{"object_id": self.storage["jontent_id"], "handle": "responses"})

        self.storage["private_response_id"] = ret
        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT2_EMAIL, settings.STUDENT2_PASSWORD)
    def test30_unauthorized_jcomment(self):
        ret = self.post(
            "jaction",
            data={
                "text": "Student2 trying to comment on L2"
            },
            **{"object_id": self.storage["private_response_id"], "handle": "comments"})

        self.assertRaises(Exception)

    @authorize(settings.INSTRUCTOR_EMAIL, settings.INSTRUCTOR_PASSWORD)
    def test31_ins_private_response(self):
        ret = self.post(
            "jaction",
            data={
                "title": "Private L1 by Instructor",
                "text": "",
                "privacy": "private"
            },
            **{"object_id": self.storage["jontent_id"], "handle": "responses"})

        self.storage["private_response_id"] = ret
        self.assertIsNotNone(ret)

    @authorize(settings.STUDENT_EMAIL, settings.STUDENT_PASSWORD)
    def test32_unauthorized_jcomment(self):
        ret = self.post(
            "jaction",
            data={
                "text": "Student2 trying to comment on L2"
            },
            **{"object_id": self.storage["private_response_id"], "handle": "comments"})

        self.assertRaises(Exception)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UserCount)
    unittest.TextTestRunner(verbosity=2).run(suite)

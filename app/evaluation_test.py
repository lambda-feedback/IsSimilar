import unittest

from .evaluation import evaluation_function


class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_absolute_lower_incorrect(self):
        body = {
            "response": 1.40,
            "answer": 1.48,
            "params": {
                "atol": 0.04
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)

    def test_absolute_lower_correct(self):
        body = {
            "response": 1.46,
            "answer": 1.48,
            "params": {
                "atol": 0.04
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_absolute_equal_correct(self):
        body = {
            "response": 1.46,
            "answer": 1.46,
            "params": {
                "atol": 0.04
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_absolute_higher_correct(self):
        body = {
            "response": 1.49,
            "answer": 1.48,
            "params": {
                "atol": 0.04
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_absolute_higher_incorrect(self):
        body = {
            "response": 1.54,
            "answer": 1.48,
            "params": {
                "atol": 0.04
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)

    def test_relative_lower_incorrect(self):
        body = {
            "response": 9.1,
            "answer": 11.4,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)

    def test_relative_lower_correct(self):
        body = {
            "response": 10.8,
            "answer": 11.4,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_relative_equal_correct(self):
        body = {
            "response": 11.4,
            "answer": 11.4,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_relative_higher_correct(self):
        body = {
            "response": 13.2,
            "answer": 11.4,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_relative_higher_incorrect(self):
        body = {
            "response": 13.7,
            "answer": 11.4,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)

    def test_relative_absolute_correct(self):
        body = {
            "response": 1e6,
            "answer": 1e7,
            "params": {
                "rtol": 1e-1,
                "atol": 8.2e6
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), True)

    def test_relative_absolute_incorrect(self):
        body = {
            "response": 1e6,
            "answer": 2e7,
            "params": {
                "rtol": 1e-1,
                "atol": 8.2e6
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)

    def test_possible_bug_with_atol(self):
        response_low = 15.7
        response_high = 15.9
        response_under = 15.6999999
        response_over = 15.90000001
        answer = 15.8
        params = {"atol": 0.1}

        result_low = evaluation_function(response_low, answer, params)
        result_high = evaluation_function(response_high, answer, params)

        self.assertEqual(result_low.get("is_correct"), True)
        self.assertEqual(result_high.get("is_correct"), True)

        result_under = evaluation_function(response_under, answer, params)
        result_over = evaluation_function(response_over, answer, params)

        self.assertEqual(result_under.get("is_correct"), False)
        self.assertEqual(result_over.get("is_correct"), False)

    def test_answer_is_not_number(self):
        body = {
            "response": 2,
            "answer": "two",
            "params": {
                "rtol": 0.2
            },
        }

        self.assertRaises(
            Exception,
            evaluation_function,
            body["response"],
            body["answer"],
            {},
        )

    def test_response_is_not_number(self):
        body = {
            "response": "two",
            "answer": 2,
            "params": {
                "rtol": 0.2
            },
        }

        response = evaluation_function(body['response'], body['answer'],
                                       body.get('params', {}))

        self.assertEqual(response.get("is_correct"), False)
        self.assertEqual("Please enter a number." in response.get("feedback"), True)

if __name__ == "__main__":
    unittest.main()

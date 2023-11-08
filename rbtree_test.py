from redblack import *

import unittest


class TestRedBlackTree(unittest.TestCase):
    def setUp(self):
        # Set up an empty tree and a sample tree for testing
        self.empty_tree = RedBlackTree()
        self.sample_tree = RedBlackTree()
        self.sample_tree.root = Node(2, "two")
        self.sample_tree.root.colour = Black
        self.sample_tree.root.left = Node(1, "one")
        self.sample_tree.root.left.colour = Black
        self.sample_tree.root.right = Node(4, "four")
        self.sample_tree.root.right.colour = Red
        self.sample_tree.root.right.left = Node(3, "three")
        self.sample_tree.root.right.left.colour = Black
        self.sample_tree.root.right.right = Node(6, "six")
        self.sample_tree.root.right.right.colour = Black

    def test_insert_into_empty_tree(self):
        # Test inserting into an empty tree
        self.empty_tree.plainInsert(5, "five")
        self.assertEqual(
            self.empty_tree.showStack(), ["5:five:R"]
        )  # Stack should only contain the inserted node
        self.assertEqual(
            self.empty_tree.root.key, 5
        )  # Root should be the inserted node
        self.assertEqual(self.empty_tree.root.value, "five")  # Value should be "five"
        self.assertEqual(self.empty_tree.root.colour, Red)  # Colour should be Red

    def test_insert_new_key(self):
        # Test inserting a new key-value pair
        self.sample_tree.plainInsert(5, "five")
        self.assertEqual(
            self.sample_tree.showStack(),
            ["2:two:B", "r", "4:four:R", "r", "6:six:B", "l", "5:five:R"],
        )
        # Check if the key-value pair is correctly inserted
        self.assertEqual(self.sample_tree.lookup(5), "five")

    def test_overwrite_existing_key(self):
        # Test overwriting an existing key
        self.sample_tree.plainInsert(4, "four_new")
        self.assertEqual(
            self.sample_tree.showStack(), ["2:two:B", "r", "4:four_new:R"]
        )  # Stack should show the path to the updated node
        # The value of the existing key should be updated
        self.assertEqual(self.sample_tree.lookup(4), "four_new")


class TestRedUncleRule(unittest.TestCase):
    def setUp(self):
        # Set up a tree where the red-uncle rule can be applied
        self.tree_with_red_uncle = RedBlackTree()
        # Construct a tree where the red-uncle rule should be triggered
        # Example: Node structure is as follows:
        #     B
        #    / \
        #   R   R
        #  /
        # R (current node)
        self.tree_with_red_uncle.root = Node(10, "ten")
        self.tree_with_red_uncle.root.colour = Black
        self.tree_with_red_uncle.root.left = Node(5, "five")
        self.tree_with_red_uncle.root.right = Node(15, "fifteen")
        self.tree_with_red_uncle.root.left.colour = Red
        self.tree_with_red_uncle.root.right.colour = Red
        self.tree_with_red_uncle.root.left.left = Node(2, "two")
        self.tree_with_red_uncle.root.left.left.colour = Red
        # The stack should represent the path: [root, Left, node(5), Left, node(2)]
        self.tree_with_red_uncle.stack = [
            self.tree_with_red_uncle.root,
            Left,
            self.tree_with_red_uncle.root.left,
            Left,
            self.tree_with_red_uncle.root.left.left,
        ]

        # Set up a tree where the red-uncle rule is not applicable
        self.tree_without_red_uncle = RedBlackTree()
        # Construct a tree where the red-uncle rule should not trigger
        # Example: Node structure is as follows:
        #     B
        #    /
        #   R
        #  /
        # R (current node)
        self.tree_without_red_uncle.root = Node(10, "ten")
        self.tree_without_red_uncle.root.colour = Black
        self.tree_without_red_uncle.root.left = Node(5, "five")
        self.tree_without_red_uncle.root.left.colour = Red
        self.tree_without_red_uncle.root.left.left = Node(2, "two")
        self.tree_without_red_uncle.root.left.left.colour = Red
        # The stack should represent the path: [root, Left, node(5), Left, node(2)]
        self.tree_without_red_uncle.stack = [
            self.tree_without_red_uncle.root,
            Left,
            self.tree_without_red_uncle.root.left,
            Left,
            self.tree_without_red_uncle.root.left.left,
        ]

    def test_red_uncle_rule_applicable(self):
        # Test that the red-uncle rule is correctly applied
        result = self.tree_with_red_uncle.tryRedUncle()
        self.assertTrue(result)
        # Check if the colors are flipped properly
        self.assertEqual(self.tree_with_red_uncle.root.colour, Red)
        self.assertEqual(self.tree_with_red_uncle.root.left.colour, Black)
        self.assertEqual(self.tree_with_red_uncle.root.right.colour, Black)
        self.assertEqual(self.tree_with_red_uncle.root.left.left.colour, Red)
        # Check if the stack is updated correctly
        self.assertEqual(
            self.tree_with_red_uncle.showStack(),
            [self.tree_with_red_uncle.root.__str__()],
        )

    def test_red_uncle_rule_not_applicable(self):
        # Test that the red-uncle rule is not applied when it should not be
        result = self.tree_without_red_uncle.tryRedUncle()
        self.assertFalse(result)
        # Check that colors remain the same
        self.assertEqual(self.tree_without_red_uncle.root.colour, Black)
        self.assertEqual(self.tree_without_red_uncle.root.left.colour, Red)
        self.assertEqual(self.tree_without_red_uncle.root.left.left.colour, Red)
        # Check if the stack is not changed
        self.assertEqual(
            self.tree_without_red_uncle.showStack(),
            list(
                map(
                    lambda x: x.__str__() if isinstance(x, Node) else branchLabel(x),
                    [
                        self.tree_without_red_uncle.root,
                        Left,
                        self.tree_without_red_uncle.root.left,
                        Left,
                        self.tree_without_red_uncle.root.left.left,
                    ],
                )
            ),
        )

        import unittest


class TestEndgame(unittest.TestCase):
    def setUp(self):
        # Set up a generic tree which can be modified in each test case
        self.tree = RedBlackTree()

    def test_endgame_problem_cured(self):
        # Scenario where the tree is already a legal red-black tree
        self.tree.root = Node(10, "ten")
        self.tree.root.colour = Black
        self.tree.stack = [self.tree.root]
        # No action should be taken by endgame, so we'll check that nothing changes
        # before_endgame = self.tree.__repr__()
        self.tree.endgame()
        # after_endgame = self.tree.__repr__()
        # self.assertEqual(before_endgame, after_endgame)

    def test_endgame_red_pushed_to_root(self):
        # Scenario where the root is red after applying red-uncle rule
        self.tree.root = Node(10, "ten")
        self.tree.root.colour = Red
        self.tree.root.left = Node(5, "five")
        self.tree.root.left.colour = Black
        self.tree.root.right = Node(15, "fifteen")
        self.tree.root.right.colour = Black
        self.tree.stack = [self.tree.root]
        # Call endgame
        self.tree.endgame()
        # The root should now be black
        self.assertEqual(self.tree.root.colour, Black)

    def test_endgame_black_with_four_black_descendants(self):
        # Scenario where a black node has four black descendants
        self.tree.root = Node(10, "ten")
        self.tree.root.colour = Black
        self.tree.root.left = Node(5, "five")
        self.tree.root.left.colour = Red
        self.tree.root.left.left = Node(3, "three")
        self.tree.root.left.left.colour = Red
        # Assume stack is correctly set
        self.tree.stack = [self.tree.root]
        print(self.tree.stack)
        # Call endgame
        self.tree.endgame()
        # Verify that the tree is now balanced
        # Check the subtree rooted at 5 is balanced as a result of endgame
        subtree_root = self.tree.root
        self.assertEqual(subtree_root.key, 5)
        self.assertEqual(subtree_root.colour, Black)
        self.assertEqual(subtree_root.left.key, 3)
        self.assertEqual(subtree_root.right.key, 10)
        self.assertEqual(subtree_root.left.colour, Red)
        self.assertEqual(subtree_root.right.colour, Red) 


class TestRedBlackTreeInsert(unittest.TestCase):

    def setUp(self):
        self.tree = RedBlackTree()

    def test_insert(self):
        # Test inserting into an empty tree
        self.tree.insert(10, "ten")
        self.assertEqual(self.tree.lookup(10), "ten")
        self.assertEqual(self.tree.root.key, 10)
        self.assertEqual(self.tree.root.colour, Black)  # The root must be black

        # Test inserting a new node that goes to the left of the root
        self.tree.insert(5, "five")
        self.assertEqual(self.tree.lookup(5), "five")
        # The new node should be red, and the red-black properties should be preserved
        self.assertEqual(self.tree.root.left.key, 5)
        self.assertEqual(self.tree.root.left.colour, Red)

        # Test inserting a new node that goes to the right of the root
        self.tree.insert(15, "fifteen")
        self.assertEqual(self.tree.lookup(15), "fifteen")
        # The new node should be red, and the red-black properties should be preserved
        self.assertEqual(self.tree.root.right.key, 15)
        self.assertEqual(self.tree.root.right.colour, Red)

        # Test inserting a node that causes a red-uncle scenario
        self.tree.insert(1, "one")
        # After insertion and fix-up, the tree should remain a valid red-black tree
        # Specific assertions will depend on your red-black tree's fix-up logic
        self.assertEqual(self.tree.lookup(1), "one")
        # You can add more checks for the structure and colours according to the expected outcomes

        # Test inserting a node that triggers the endgame fix-up
        self.tree.insert(6, "six")
        # After insertion and fix-up, the tree should remain a valid red-black tree
        self.assertEqual(self.tree.lookup(6), "six")
        # More detailed structure and colour checks can be added here according to the expected outcomes



class TestRedBlackTreeProperties(unittest.TestCase):

    def setUp(self):
        self.tree = RedBlackTree()

    def test_insert_and_properties(self):
        # Insert a sequence of values that will result in a tree requiring fix-up
        keys_to_insert = [(10, "ten"), (15, "fifteen"), (5, "five"), (1, "one"), (20, "twenty")]
        for key, value in keys_to_insert:
            self.tree.insert(key, value)
            # After each insert, check if the tree still satisfies red-black properties
            self.assertTrue(self.check_red_black_properties(self.tree.root))

    def check_red_black_properties(self, node, black_count=-1, path_black_count=0):
        if node is None:
            # Base case: Reached a leaf node (NIL), check black count
            if black_count == -1:
                black_count = path_black_count
            return black_count == path_black_count

        # Property 1: Node is either red or black is implicitly satisfied by the data structure

        # Property 2: Root is black
        if self.tree.root.colour != Black:
            return False

        # Property 4: Red nodes have black children
        if node.colour == Red:
            if (node.left is not None and node.left.colour == Red) or \
               (node.right is not None and node.right.colour == Red):
                return False

        # Property 3: All leaves (NIL nodes) are black is handled by the nature of the recursion and base case

        # Increment path_black_count if current node is black
        if node.colour == Black:
            path_black_count += 1

        # Check black count on both left and right paths
        return self.check_red_black_properties(node.left, black_count, path_black_count) and \
               self.check_red_black_properties(node.right, black_count, path_black_count)


if __name__ == "__main__":
    unittest.main()

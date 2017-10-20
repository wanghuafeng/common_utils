#!-*- coding:utf-8 -*-

class BinaryTreeNode:
    """
    二叉树查找的性质：
    若任意节点的左子树不空，则左子树上所有结点的值均小于它的根结点的值；
    任意节点的右子树不空，则右子树上所有结点的值均大于它的根结点的值；
    任意节点的左、右子树也分别为二叉查找树。
    没有键值相等的节点
    """
    def __init__(self, val):
        self.left = None
        self.right = None
        self.data = val

    def insert_node(self, data):
        if data < self.data:
            if self.left is None:
                self.left = BinaryTreeNode(data)
            else:
                self.left.insert_node(data)
        elif data > self.data:
            if self.right is None:
                self.right = BinaryTreeNode(data)
            else:
                self.right.insert_node(data)

    def search_val(self, data):
        if data < self.data:
            if self.left is None:
                return None
            return self.left.search_val(data)
        elif data > self.data:
            if self.right is None:
                return None
            return self.right.search_val(data)
        else:
            return self

class BiSearch(object):
    """
    有序数组二分查找
    时间复杂度：O(logn)
    """
    def bi_search(self, l, val):
        """循环方式实现"""
        start = 0
        end = len(l) - 1
        while start <= end:
            mid = (start + end) / 2
            print mid, l[mid]
            if val > l[mid]:
                start = mid + 1
            elif val < l[mid]:
                end = mid - 1
            else:
                return mid
        return False

    def search(self, l, val, s, e):
        """
        递归方式
        """
        if s > e:
            return False
        mid = (s + e) / 2
        if val > l[mid]:
            s = mid + 1
            return self.search(l, val, s, e)
        elif val < l[mid]:
            e = mid - 1
            return self.search(l, val, s, e)
        else:
            return mid

class Fibonacci(object):
    """
    '1 1 2 3 5 8 13'
    斐波那契数列实现
    """

    def fibonacci(self, n):
        """
        迭代方式实现
        """
        if n <= 2:
            return 1
        a, b = 1, 1
        for i in range(n - 2):
            a, b = b, a + b
        return b

    def fibonacci_recu(self, n):
        """递归方式实现"""
        if n <= 2:
            return 1
        return self.fibonacci_recu(n - 1) + self.fibonacci_recu(n - 2)


class twoSum(object):
    """
    Given nums = [2, 7, 11, 15], target = 9,
    Because nums[0] + nums[1] = 2 + 7 = 9,
    return [0, 1].
    返回满足条件数组元素下标
    展开：
        1、只返回两个元素
        2、返回两个元素以及他们的数组下标
    """

    def two_sum(self, nums, target):
        if len(nums) <= 1:
            return False
        buff_dict = {}
        for i in range(len(nums)):
            if nums[i] in buff_dict:
                return [buff_dict[nums[i]], i]
            else:
                buff_dict[target - nums[i]] = i

    def ret_two_num_without_index(self, l, target):
        """仅返回元素，不需要元素下标"""
        # l = [1,2,3,4,5,6,7,8,9,0]
        # target = 3
        d = {}
        for i in range(len(l)):
            if d.get(l[i]):
                return l[i], d.get(l[i])    # 这里假设只有一组num之和为target，若非，则可将它们放到一个tuple中
            else:
                d[target-l[i]] = l[i]

    def ret_num_index(self, l, target):
        """返回满足条件元素的下标"""
        # l = [1,2,3,4,5,6,7,8,9,0]
        # target = 3
        d = {}
        for i in range(len(l)):
            if d.get(l[i]) is not None: # index为0时此处为False，所以用is not None进行判断
                return i, d.get(l[i])    # 这里假设只有一组num之和为target，若非，则可将它们放到一个tuple中
            else:
                d[target-l[i]] = i

class LengthOfLongestSubstring(object):
    """
    给定一个字符串，找其无重复字符的最长子串的长度。
    例如：
        "abcabcbb"的无重复字符的最长子串是"abc"，长度为3
        "bbbbb"的无重复字符的最长子串是"b"，长度为1
    """
    def get_length(self, s):
        start = maxLength = 0
        usedChar = {}
        for i in range(len(s)):
            if s[i] in usedChar and start <= usedChar[s[i]]:
                start = usedChar[s[i]] + 1
            else:
                maxLength = max(maxLength, i - start + 1)

            usedChar[s[i]] = i

        return maxLength

    def get_length_(self, s):
        """
        思路：
            细化到某一个字符，距上次出现的最大长度
        """
        if not s: return 0
        marked_char_dic = {}
        max_length = 1
        for index in range(len(s)):
            char = s[index]
            if marked_char_dic.get(char) is not None:
                str_len = index - marked_char_dic.get(char)
                max_length = str_len if str_len > max_length else max_length
            marked_char_dic[char] = index
        return max_length
print LengthOfLongestSubstring().get_length_('aab')
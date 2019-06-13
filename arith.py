#!-*- coding:utf-8 -*-
"""
--------------------readline,readlines,read占用内存分析---------------------------
原始语料：546M
1.readlines()
    with codecs.open(combine_bigram_remove_freq_1_filename, encoding='utf-8') as f:
        temp_list = [item for item in f.readlines()]
CPU usage：34.6% ==> 61.7%
占用内存：2.168G
耗时：5.66499996185s
2.
    with codecs.open(combine_bigram_remove_freq_1_filename, encoding='utf-8') as f:
        temp_list = [item for item in f]
CPU usage：35.3% ==> 62.0%
占用内存：2.136G
耗时：48.2940001488s
3.read()
    with codecs.open(combine_bigram_remove_freq_1_filename, encoding='utf-8') as f:
        temp_str =f.read()
CPU usage：30.4% ==> 36.3%
占用内存：0.48G
耗时：48.2940001488s
4.readline()
f = codecs.open(filename, encoding='utf-8')
start_time = time.time()
while 1:
    line = f.readline()
    if not line:
        end_time = time.time()
        print end_time-start_time
        break
耗时：50.6809999943
--------------------字典for in 性能测试---------------------------
d = {}
for i in range(100000000):
    d['%s'%i] = None
print len(d)#100000000
start_time = time.time()
print 'a' in d#False
print "in time consume: ", time.time() - start_time#in time consume:  0.0

start_time = time.time()
print d.get('a')     #None
print "get: ", time.time() - start_time     #get:  0.0

start_time = time.time()
print 'a' in d.keys()#False
print 'd.keys time consume: ', time.time() - start_time#d.keys time consume:  9.39199995995

测试结论：
     1、使用字典的in操作查找的时间复杂度为O(1)
     2、get操作的时间负责度为O(1)

--------------------python write, writelines性能分析--------------------------
准备数据：1G文本数据(共：5193374行)
1.write()
with open() as wf:
  wf.write(line)
性能分析：写数据耗时：13.094s
写入速度：6610.373708059671（行/秒）

2.writelines()
with open() as wf:
  wf.writelines([line_list])
性能分析：写数据耗时：8.226s
若对line_list进行列表解析操作，遍历1G列表耗时：0.4s     (5,193,374行)
写入速度：10522.27490072129（行/秒）

3.fileObj = open()
fileObj.write()
性能分析：写数据耗时：12.812s

对比1、3可知，with操作在对每行文件写操作完成以后有额外的操作：__exit__()将wf资源释放
--------------------python数据结构内存占用分析-----------------------
字典（dict）：
原始语料：546M
CPU usage：36.7% ==> 76.9%
占用内存3.2G     （占用空间为原始语料的6倍）
查找时间复杂度：O(1)

集合（set）：
原始语料：546M
CPU usage：34.6%==>70.6%
占用内存：2.88G     （占用空间为原始语料的5.4倍）
查找时间复杂度：O(1)

数组（List）：
原始语料：546M
CPU usage：34.9%==>60.6%
占用内存：2.05G     （占用空间为原始语料的3.85倍）
查找时间复杂度：O(n)
"""
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
        """递归方式"""
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

# print LengthOfLongestSubstring().get_length_('aab')
def insert_sort(lists):
    """
    从左到右遍历数组, 将每个元素插入它左边已排好序数组
    """
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists


def bubble_sort(lists):
    """
    两层循环
    """
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    return lists

def quick_sort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]      #将第一个值做为基准
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)

        less = quick_sort(less)      #得到第一轮分组之后，继续将分组进行下去。
        more = quick_sort(more)
        return less + pivotList + more

class Solution(object):
    def removeDuplicates(self, nums):
        """
        26题
        :type nums: List[int]
        :rtype: int
        """
        # 删除列表中的重复项，返回操作后的长度
        # [1,1,1,2,3,4,4,4,5] -> [1,2,3,4,5] 5
        # 维护2个索引，慢的s，快的f；s指向第一个元素，f的指向第二个元素;
        # 判断f和f前一个元素是否相等，相等则f后移；不等则s后移一个，值给s，然后f也后移
        if len(nums) <= 1:
            return len(nums)

        s = 0

        for f in range(1, len(nums)):
            if nums[s] != nums[f]:
                s += 1
                nums[s] = nums[f]
        return s + 1
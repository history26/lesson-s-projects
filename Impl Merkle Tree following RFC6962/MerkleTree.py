import hashlib
import random
import string
import copy


# 定义叶节点
class Node:
    def __init__(self):
        # 每个节点的元素包括父节点和左右子节点，及value和对应的hash值
        self.value = None
        self.hash = None
        self.leftNode = None
        self.rightNode = None
        self.parent = None

    # 计算hash值
    def calculator(self, tmp: str):
        return hashlib.sha256(tmp.encode('utf-8')).hexdigest()


# 定义Merkle_Tree:
class Merkle_Tree:
    def __init__(self, leaf: list[Node]):  # 创建merkle tree时传入一个包含叶节点的列表类型
        # 定义叶节点
        self.leaf = leaf
        self.root = Node()
        self.listofnodes = []

    def print_root(self):
        print("root: ", self.root)
        print("value", self.root.value)
        print("hash", self.root.hash)

    def create_tree(self):
        leaf_nodes = copy.deepcopy(self.leaf)
        while len(leaf_nodes) > 1:
            parent_nodes = []
            for i in range(0, len(leaf_nodes), 2):
                lfnodes = leaf_nodes[i]
                lfnodes.hash = lfnodes.calculator(lfnodes.value)
                if i + 1 < len(leaf_nodes):
                    rtnodes = leaf_nodes[i + 1]
                    rtnodes.hash = rtnodes.calculator(rtnodes.value)
                else:
                    parent_nodes.append(leaf_nodes[i])
                    break
                # 父节点的value值等于左右子节点的hash值
                p = Node()
                lfnodes.parent = p
                rtnodes.parent = p
                p.leftNode = lfnodes
                p.rightNode = rtnodes
                p.value = lfnodes.hash + rtnodes.hash
                p.hash = p.calculator(p.value)
                parent_nodes.append(p)
            leaf_nodes = parent_nodes
        self.root = copy.deepcopy(leaf_nodes[0])

    # check inclusion or exclusion

    def order(self, root: Node):
        self.listofnodes.append(root.hash)
        self.check(root.leftNode)
        self.check(root.rightNode)

    def check(self, check_hash: str):
        if check_hash in self.listofnodes:
            print(" specified element is inclusion ")
        else:
            print(" specified element is exclusion ")


if __name__ == "__main__":
    ls_nodes = []
    raw_str = "qwertyuioplkjhgfdsazxcvbnm1230456789"
    check_hash = ''  # 随机选取一个字符串当作hash并查看是否在树种
    for i in range(64):
        check_hash = ''.join(random.choice(raw_str))
    # 生成100k个叶节点
    for i in range(100000):
        n = Node()
        n.value = ''.join(random.sample(string.ascii_letters, 8))
        ls_nodes.append(n)
    mymerkletree = Merkle_Tree(ls_nodes)
    mymerkletree.create_tree()
    mymerkletree.print_root()
    mymerkletree.order(mymerkletree.root)
    mymerkletree.check(check_hash)
    mymerkletree.check(mymerkletree.root.hash)

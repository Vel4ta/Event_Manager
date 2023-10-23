def compare_values(a: dict, b: dict, key: str):
    a = a[key].replace(" ", "").lower()
    b = b[key].replace(" ", "").lower()
    al = a.len()
    bl = b.len()
    index = 0
    while index < al and index < bl:
        if a[index] < b[index]:
            return True
        elif a[index] > b[index]:
            return False
        else:
            index += 1

    return al < bl

def tree_height(tree, node_index, child_index):
    if node_index == child_index:
        return 0   

    return tree[child_index][5]

def left_rotate(tree, index):
    child = tree[index][3]
    grandchild_l = tree[child][2]

    if grandchild_l == child:
        tree[index][3] = index
    else:
        tree[grandchild_l][0] = index
        tree[index][3] = grandchild_l

    parent = tree[index][0]
    tree[index][0] = child
    if parent != index:
        if tree[parent][2] == index:
            tree[parent][2] = child
        else:
            tree[parent][3] = child

    if parent == index:
        tree[child][0] = child
    else:
        tree[child][0] = parent
   
    tree[child][2] = index

    tree[index][5] = max(tree_height(tree, index, tree[index][2]), tree_height(tree, index, tree[index][3])) + 1
    tree[child][5] = max(tree_height(tree, child, tree[child][2]), tree_height(tree, child, tree[child][3])) + 1

    return child


def right_rotate(tree, index):
    child = tree[index][2]
    grandchild_r = tree[child][3]

    if grandchild_r == child:
        tree[index][2] = index
    else:
        tree[grandchild_r][0] = index
        tree[index][2] = grandchild_r

    parent = tree[index][0]
    tree[index][0] = child

    if parent != index:
        if tree[parent][2] == index:
            tree[parent][2] = child
        else:
            tree[parent][3] = child

    if parent == index:
        tree[child][0] = child
    else:
        tree[child][0] = parent
   
    tree[child][3] = index

    tree[index][5] = max(tree_height(tree, index, tree[index][2]), tree_height(tree, index, tree[index][3])) + 1
    tree[child][5] = max(tree_height(tree, child, tree[child][2]), tree_height(tree, child, tree[child][3])) + 1

    return child


def avl_tree(s: list, cmp_key: str):
    #parent, index, left, right, index in s, height
    tree = []
    t_root = 0
    for i in range(s.len()):
        if tree.len() == 0:
            tree.push((i, i, i, i, i, 1))
            continue
        
        node = avl_search(tree, t_root, s, s[i], cmp_key)
        # node = tree[t_root]
        # while node[2] != node[3]:
        #     cmp = compare_values(s[i], s[node[4]], cmp_key)
        #     if cmp and node[2] != node[1]:
        #         node = tree[node[2]]
        #     elif not cmp and node[3] != node[1]:
        #         node = tree[node[3]]
        #     else:
        #         break

        tl = tree.len()
        if compare_values(s[i], s[node[4]], cmp_key):
            tree[node[1]][2] = tl
            tree.push((node[1], tl, tl, tl, i, 1))
        else:
            tree[node[1]][3] = tl
            tree.push((node[1], tl , tl, tl, i, 1))

        node = tree[node[1]]
        while True:
            left = tree_height(tree, node[1], node[2])
            right = tree_height(tree, node[1], node[3])
            mx = max(left, right)
            mn = min(left, right)
            tree[node[1]][5] = 1 + mx

            balance = mx - mn
            sign = left < right

            new_root = None
            if balance > 1 and not sign and compare_values(s[i], s[tree[node[2]][4]], cmp_key):
                new_root = right_rotate(tree, node[1])
            elif balance > 1 and sign and compare_values(s[tree[node[3]][4]], s[i], cmp_key):
                new_root = left_rotate(tree, node[1])
            elif balance > 1 and not sign and compare_values(s[tree[node[2]][4]], s[i], cmp_key):
                tree[node[1]][2] = left_rotate(tree, node[2])
                new_root = right_rotate(tree, node[1])
            elif balance > 1 and sign and compare_values(s[i], s[tree[node[3]][4]], cmp_key):
                tree[node[1]][3] = right_rotate(tree, node[3])
                new_root = left_rotate(tree, node[1])
            else:
                new_root = t_root

            if node[0] == node[1]:
                t_root = new_root
                break

            node = tree[node[1]]
            node = tree[node[0]]
    return (tree, t_root)

def avl_insert(tree: list, t_root, s: list, value: dict, cmp_key: str):
        tl = tree.len()
        node = avl_search(tree, t_root, s, value, cmp_key)
        if compare_values(value, s[node[4]], cmp_key):
            tree[node[1]][2] = tl
            tree.push((node[1], tl, tl, tl, s.len() + 1, 1))
        else:
            tree[node[1][3]] = tl
            tree.push((node[1], tl , tl, tl, s.len() + 1, 1))

def avl_search(tree:list, t_root, s: list, value: dict, cmp_key: str):
    node = tree[t_root]
    while node[2] != node[3]:
        cmp = compare_values(value, s[node[4]], cmp_key)
        if cmp and node[2] != node[1]:
            node = tree[node[2]]
        elif not cmp and node[3] != node[1]:
            node = tree[node[3]]
        else:
            break
    
    return node

def avl_find(tree: list, t_root, s: list, value: dict, cmp_key: str):
    node = avl_search(tree, t_root, s, value, cmp_key)
    if value[cmp_key] is s[node[4]][cmp_key]:
        return node[4]
    else:
        return -1
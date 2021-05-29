import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# 数据分析以及整理

# 读取csv文件的函数
def read_csv():
    huxing_list=[]
    area_list=[]
    # 这里需要改成您自己的文件的路径，使用绝对路径就可以，并将从csv中读取的数据转化成为一个dataframe对象，这个对象是pandas中用于读取数据的对象
    df=pd.read_csv("武汉出租房源情况.csv")
    # 去重
    df1 = df.drop_duplicates(subset=["房屋描述","房屋地址","房屋详情（户型）以及经纪人"],inplace=False)
    # 使用上一步获取的df对象，根据每一列的列头读取相应的数据，并转成list存储，下面三步一样的操作
    price_list=df1['房屋价格'].tolist()
    detail_list=df1['房屋详情（户型）以及经纪人'].tolist()
    address_list=df1['房屋地址'].tolist()
    # 因为在csv中房屋详情这里是有经纪人的干扰因素的，所以这里通过使用“|”作为分界符，将类似“3室2厅|12平米|中层(共32层) 杨凯奇”的数据切割成“[3室2厅,12平米,中层(共32层) 杨凯奇]”这样的
    # list数据，然后我们取list中的第一个和第二个，分别加入到huxing_list和area_list两个list中。
    for i in detail_list:
        huxing_list.append(i.split("|")[0])
        area_list.append(i.split("|")[1])
    # 返回address_list，huxing_list，area_list，price_list
    return address_list,huxing_list,area_list,price_list

# 这个函数是将输入的列表转化为字典并输出
# 这个方法的作用主要是为了做统计。以huxing_list为例子的话就是，统计每种户型的数量，其中字典的key就是每种户型，value就是每种户型对应的个数
def list_to_dict(list,item_list=None):
    # 初始化字典
    dict={}
    # 这里的item_list是用来做参照的，后面会传入地区的列表，如果没有传入就做普通的统计工作
    if item_list==None:
        # 还是以huxing_list为例子，遍历传入的列表，并查询字典中是否已经含有相应户型，如果含有了，就用该户型作为key找到相应的value（个数），并对value做加1的处理
        # 如果没找到相应户型，那么就在字典中添加一个该户型的字典元素，key是户型，value初始化是1，因为既然已经遍历到了，那么就证明有这种户型的至少存在一个
        for i in list:
            if dict.__contains__(i):
                dict[i] += 1
            else:
                dict[i] = 1
        return dict
    # 这里是有item_list作为参照的，即会传入地区列表作为参照，因为您的需求里面有统计每个区域的房源数量，所以这里需要一个辅助的地区list
    else:
        # 遍历地区列表，以每个地区为key，初始化字典，这里value指的是房源数量，所以初始化的时候可以为0，即这个地区没有相应房源的时候为0
        for i in item_list:
            dict[i]=0
        # 遍历地区列表同时在里面遍历地址列表，判断地址里是否含有相应的地区名，如果含有，证明该房源是属于该地区的，那么该地区的value+1
        for j in item_list:
            for i in list:
                if i.__contains__(j):
                    dict[j]+=1
        return dict

# 该函数用于计算平均价格，对应第三个需求，传入的参数分别是，地区的房源数量字典，不同房源价格列表，与价格列表对应的地址列表
# 基本逻辑就是：因为价格列表和地址列表是一一对应的关系，所以可以通过地址列表判断不同的价格属于哪个地区，然后做加法，最后用每个地区的总价格除以房源数量
def average_price(num_dict,price_list,address_list):
    # 参数中的房源数量字典 key：地区，value：该地区房源数量
    # 地址与价格一一对应的字典 key：地址，value：价格
    # address_price_dict={}
    # 地区和每个地区总价一一对应的字典 key：地区，value：地区总价
    area_sum_price_dict={}
    # 每个地区平均价格字典 key：地区，value：地区平均价格
    average_price_dict={}
    # 以地址列表的长度为条件，遍历价格列表和地址列表，并按55行给出的结构初始化字典
    # for i in range(len(address_list)):
    #     address_price_dict[address_list[i]]=price_list[i]
    # 遍历房源数量字典，使用房源数量字典的key作为area_sum_price_dict的key，初始化字典，value=0，即地区总价一开始为0
    for i in num_dict:
        area_sum_price_dict[i] = 0
        # 遍历 地址与价格的字典，如果该字典中的key，即地址，中包含相应的房源数量字典的key，即地区，那么就把该地址对应的价格加到相应地区的字典的value上
        for j in range(len(address_list)):
            # print(j)
            if address_list[j].__contains__(i+"-"):
                area_sum_price_dict[i]+=price_list[j]
                    # print(j)
        # 判断地区房源数量字典各个地区对应的房源数量是否为0，如果为0那么证明该地区没有房源，也就没有对应的价格，那么该地区对应的房源平均价就为0
        # 如果该地区的房源数量不为0，那么我们就用地区总价格除以房源数量并保留两位小数，并把它作为value传入到相应的平均价格字典中
        if num_dict[i]!=0:
            average_price_dict[i]=round(area_sum_price_dict[i]/num_dict[i],2)
        else:
            average_price_dict[i]=0
    # 返回平均价格字典
    return average_price_dict

# 该函数是用来把传入的字典分别转换为key value两个list的，因为在使用matplotlib库进行画图时，参数只能传入list
def dict_to_list(dict):
    # 用来保存key的list
    key_list=[]
    # 用来保存value的list
    value_list=[]
    # 遍历字典，并分别向两个不同的list中存入相应的元素
    for i in dict:
        key_list.append(i)
        value_list.append(dict[i])
    return key_list,value_list

# 地区列表，这个是直接从网页上复制下来的
address_area_list=["洪山","武昌","江岸","汉阳","江夏","江汉","东西湖","硚口","黄陂","沌口开发区","青山",'蔡甸',"新洲"]
# 调用第一个函数，获取四个不同的list
result=read_csv()
# 通过上一步获取的result获取相应的列表
address_list=result[0]
huxing_list=result[1]
area_list=result[2]
price_list=result[3]

# 调用上面的list_to_dict函数，用来统计户型的数量
huxing_dict=list_to_dict(huxing_list)

# 用来统计房屋面积相应的数量
area_dict=list_to_dict(area_list)

# 统计区域房源数量，所以需要把第二个参数：地区列表加上
address_num_dict=list_to_dict(address_list,address_area_list)

# 统计区域房源平均价格
average_price_dict=average_price(address_num_dict,price_list,address_list)

# 输出
print(address_num_dict)
print(huxing_dict)
print(average_price_dict)
print(area_dict)

# 将上面获取到的字典都转换为key，value的列表，以address_result为例，address_result[0]就是key的列表，address_result[1]就是value的列表
address_result=dict_to_list(address_num_dict)
huxing_result=dict_to_list(huxing_dict)
average_price_result=dict_to_list(average_price_dict)
area_result=dict_to_list(area_dict)

# 开始画图，这里先定义字体为等线字体
matplotlib.rc("font",family="dengxian")

# 这个函数用来给条形图添加数值用的
def add_labels(rects):
    # 遍历传入的bar对象中的每一个bar
    for rect in rects:
        # 获取每个bar的高度
        height = rect.get_height()
        # 根据高度以及宽度，在每个bar的最顶端的中间位置加上这个bar对应的数据的值
        plt.text(rect.get_x() + rect.get_width()/2, height+0.01*height, '%.0f'%height, ha='center',  va='bottom', fontsize=12, color='b')
        # 设置边缘显色为白色
        rect.set_edgecolor('white')

# 第一个图
# 定义一个窗口，名字叫窗口1，大小是：宽15长6
plt.figure(1,figsize=(15,6))
# 设置图的标题
plt.title("武汉区域房源总数量统计图")
# 这里由于key_list和value_list 的长度是一样的，所以第一个参数以key的长度为范围，并利用第二个参数将value_list传入，用来作为柱状图的高度
# 最后一个参数规定柱状图的每个柱的宽度是0.8
b=plt.bar(range(len(address_result[0])),address_result[1],0.8)
# 调用上面的函数，给每个柱都添加数值，即将每个柱对应的值写在柱的顶端
add_labels(b)
# 这里是设置横坐标的值，第一参数是横坐标的范围，第二个参数是横坐标对应的值，这里使用key_list作为横坐标的值
plt.xticks(range(len(address_result[0])),address_result[0])
# 以下两个函数分别规定横纵左边的坐标值
plt.xlabel("区域")
plt.ylabel("数量")


# 第二张图
# 与上面的步骤类似，这里只说明不同的点
plt.figure(2,figsize=(12,6))
plt.title("武汉区域房源户型统计图")
bar=plt.barh(range(len(huxing_result[0])),huxing_result[1],0.8)
# 这里只是把原来的那个add_labels（）函数的部分抄下来了
for i in bar:
    width=i.get_width()
    plt.text(width+10,i.get_y(),'%.0f'%width,ha='center', fontsize=12, color='b')
    i.set_edgecolor('white')
# 这里由于要画的是条形图，所以原来写在横坐标上的key_list的值，现在写到纵坐标上即可
plt.yticks(range(len(huxing_result[0])),huxing_result[0])
plt.xlabel("数量")
plt.ylabel("户型")

# 第三张图
# 与第一个类似
plt.figure(3,figsize=(12,6))
plt.title("武汉房源平均价格分析图")
# 这个函数用来画折线图，第一个参数是横坐标的值，第二个参数是纵坐标的值，并将其的颜色换为红色
plt.plot(average_price_result[0],average_price_result[1],label="平均价格",color='r')
# 这里多了个label用来规定右上角的小标签里面显示的文字
bar=plt.bar(range(len(address_result[0])),address_result[1],0.3,label="房屋数量")
add_labels(bar)
plt.xticks(range(len(address_result[0])),address_result[0])
plt.ylabel("平均价格/房屋数量")
plt.xlabel("区域")
# 这里是为了将折线图的值也都标在相应的点上，与add_labels函数类似，只不过是从柱状图变为了折线图
for a, b in zip(average_price_result[0], average_price_result[1]):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=12,color='r')
# 显示标签，即：右上角的“平均价格”和“房屋数量”
plt.legend()

# 第四张图，饼状图，由于是分析房屋占地面积的，所以比较琐碎比较多，这里我已经将图扩展到最大了，
# 也是密密麻麻，但是图本身是可以放大缩小的。右边的列表是：每种不同面积对应的颜色，左边是他对应的
# 饼状图，以及其占比
# 这一步与第一个类似，我这里固定了图的大小是：长宽都是50
plt.figure(4,figsize=(50,50))
# 这里是创建一个列表，列表的长度是面积的种类的个数，里面的所有的值都是0.02，这个值是指的每个
# 扇区之间的空隙，就是每个扇区之间的那一条小白线，这里已经调到很小了
explode=[0.02 for i in range(len(area_result[0]))]
# 创建一个饼状图，每个扇区的值都是value_list里面来的，即第一个参数，explode就是上面声明的列表，
# labels就是右边的列表，这里使用的就是key_list。autopct是在图中扇形区域的保留位数是一位
plt.pie(area_result[1],explode=explode,labels=area_result[0],autopct='%1.1f%%')
# 显示有右边的列表
plt.legend()

# 展示上面所有的图，没有这一步所有的图都不会画出来
plt.show()

#
#
#

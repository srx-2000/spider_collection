#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：config.yaml 
@File    ：zhihu_encrypt.py.py
@IDE     ：PyCharm 
@Author  ：Beier
@Date    ：2023/10/11 14:15
@github  ：https://github.com/srx-2000
'''
import hashlib
import random

import requests
from JsOperation import *
from loguru import logger

# 知乎加密逻辑复现
"""
    url_path = /api/v4/members/longgegege/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=20&limit=20
    x-zse-93 = 101_3_3.0
    # d_c0由cookie中获取，经测试这个参数依旧可以在不登录下获取，显然知乎并没有更改（乐），如果想要自动获取可以尝试使用selenium自动获取
    d_c0 = AABXNY7FGxKPTukiyJlJ_u_0H4vILACn1L0=|1603881372 
    # x-zst-81=3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZ8XY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPF0VGsQNG8hoLZqSMTGg01ugBTwLyiUX_aDNfxCoL26N8cCxKSANf5DNCDcSTvLe12cxMgGOqnwN0Q_cpnGVmmR3LrvHLcHwfbhwBAqLffBL_tJxmFGpmDwOCFcOMXcLxHhoGpBe1bAL_twtVXuC1BGcYwqCCCgYYYuYL-Dxm-D9_Vq39Oqfz3GoMErSYiGFMUh2VEDg8jqH9kBc_chwq1TNKLU3Ct9X1xwH_qwYBQ6CKUBCVph3_WbxB3ce9xbSprqe9Y8x9zCSM8ce8DCgBKweL24p0iUOYwwXOWrOC
    其中x-zst-81一般是没有的，经测试只有被限制之后，登录账号后可能出现，所以下面的加密中默认不使用该参数
"""
"""
基础逻辑：
    1. A_v = x-zse-93+"+"+url_path+"+"+d_c0
    2. B_v = md5(A_v)
    3. C_v = ord(B_v)  # 这里是对上面的32位MD5加密每个字符做了一个ord，得到一个32位数组
    # 将C_v与固定值组成一个48位的新的数组。其中C_v和D_v的关系应该是extends，否则会形成一个二维数组。其中的127是一个固定值
    4. D_v = [127 * random.random(), 0, C_v, 14,14,14,14,14,14,14,14,14,14,14,14,14,14] 
    5. E_v = D_v[0:15]
    6. F_v = D_v[16:48] # 这个值就是后面计算中至关重要的一个参数G[0]，结果F_v是一个32位的数组
    # 这里的base_arr是一个固定的16位数组：[48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
    7. J_v = [ E_v[i] ^ base_arr[i] ^ 42 for i in range(len(E_v)) ]
    8. K_v = __g.r(J_v) # 这个值就是后面计算中至关重要的一个参数G[1]，结果K_v是一个16位的数组。
    9. L_v = __g.x(F_v,K_v) # 这里就是上面说的至关重要的函数，结果L_v是一个32位的数组。
    10. M_v= K_v + L_v # 这里就得到了最终用于加密的48位数字数组。
    11. 基础计算流程（M_v）

基础计算流程【很多jsvm的加密最终用的都是类似的这个流程，如头条，抖音】：
    encrypt_str=""
    for i in range(len(M_v)-1, -1, -3):
        # 这里有四种算法，分别对应[0,24,16,8]的顺序循环，具体见下面代码实现，下面流程中给出的是循环流程中0对应的算法
        1. A_v = (M_v[i] ^ 58) + (M_v[i-1] << 8) + (M_v[i-2] << 16) # 此处M_v为基础逻辑中计算得出
        2. B_v = A_v & 63
        3. encrypt_str += base_str[B_v]
        4. C_v = A_v >> 6 & 63
        5. encrypt_str += base_str[C_v]
        6. D_v = A_v >> 12 & 63
        7. encrypt_str += base_str[D_v]
        8. E_v = A_v >> 18
        9. encrypt_str += base_str[E_v]
    return encrypt_str

__g.x(tt, te)【核心函数1，js定位方式，检索（注意空格也是需要的）：__webpack_unused_export__】:
参数说明：
    1. tt：即基础逻辑中传入的G[0]，是一个32位的数字数组，结尾是14个14
    2. te：即基础逻辑中传入的G[1]，是一个16位的数字数组，是通过__g.r(tt)进行过一轮计算得到的。
流程复现：
    tr=[]
    for i in range(0,2):
        tu = tt[i*16:(i+1)*16] # 将32位数组切分，16个元素为一组
        tc = [None for _ in range(0,16)]
        for j in range(0,16):
            tc[j] = tu[j] ^ te[j]
        te = __g.r(tc)
        tr = tr.extends(te)
    return tr

__g.r(tt)【核心函数2，js定位方式，检索（注意空格也是需要的）：__webpack_unused_export__】:
参数说明：
    1. tt：即基础逻辑中传入的J_v，亦或是__g.x中传入的tc
流程复现：
    te = [0 for _ in range(0,16)]
    tr = [0 for _ in range(0,36)]
    tr[0] = B_f(tt, 0)
    tr[1] = B_f(tt, 4)
    tr[2] = B_f(tt, 8)
    tr[3] = B_f(tt, 12)
    for i in range(0,32):
        ta = G_f(tr[i+1] ^ tr[i+2] ^ tr[i+3] ^ h_zk[i]) # 这里的h_zk同样也是一个固定的32位数组
        tr[ti + 4] =tr[i] ^ ta
    i_f(tr[35],te,0)
    i_f(tr[34],te,4)
    i_f(tr[33],te,8)
    i_f(tr[32],te,12)
    return te

__g.r(tt)中参与计算的相关函数：
    B_f(tt, te)参数说明：
        1. tt：16位数字数组 
        2. te：常数0,4,8,12
    B_f(tt, te)流程复现:
        return (255 & tt[te]) << 24 | (255 & tt[te + 1]) << 16 | (255 & tt[te + 2]) << 8 | 255 & tt[te + 3]

    G_f(tt)参数说明：
        1. 通过__g.r(tt)一系列亦或运算得到的一个大整数
    G_f(tt)流程复现:
        te = [0 for _ in range(0,4)]
        tr = [0 for _ in range(0,4)]
        i_f(tt, te, 0)
        # 下方的h_zb是一个固定的256位的数字数组
        tr[0] = h_zb[255 & te[0]]
        tr[1] = h_zb[255 & te[1]]
        tr[2] = h_zb[255 & te[2]]
        tr[3] = h_zb[255 & te[3]]
        ti = B_f(tr, 0)
        return ti ^ Q_f(ti, 2) ^ Q_f(ti, 10) ^ Q_f(ti, 18) ^ Q_f(ti, 24)

    Q_f(tt, te)参数说明:
        1. tt：通过B_f计算后得到的一个大整数
        2. te：常数2,10,18,24
    Q_f(tt, te)流程复现:
        return (4294967295 & tt) << te | tt >>> 32 - te

    i_f(tt, te, tr)参数说明：
        1. tt：大整数
        2. te：数组
        3. tr：常数0,4,8,12
    i_f(tt, te, tr)流程复现：
        te[tr] = 255 & tt >>> 24
        te[tr + 1] = 255 & tt >>> 16
        te[tr + 2] = 255 & tt >>> 8
        te[tr + 3] = 255 & tt
"""
x_zse_93 = "101_3_3.0"

# 基础加密字符串，每次从中选择一个字母，最终拼接成加密结果
base_str = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE"
# 用于计算后续的G数组中的G[1]，那个16位的数组。
base_arr = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
# 在函数__g.r中使用
h_zk = [1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157, 1933479194,
        -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428, -2029270069, 2035090028,
        -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135, 1321810770, 456816404, -1391643889,
        -229302305, 330002838, -788960546, 363569021, -1947871109]
# 在函数G_f中使用
h_zb = [20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93, 252,
        205, 90, 79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80, 189,
        71, 191, 97, 84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22, 255,
        94, 238, 151, 85, 77, 124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146, 162,
        62, 224, 218, 196, 229, 1, 192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117,
        228, 215, 203, 53, 239, 251, 127, 81, 11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122,
        145, 106, 118, 74, 190, 29, 16, 174, 5, 177, 129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68,
        207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244, 155, 51, 236, 200, 233, 58, 61, 47, 100, 137,
        185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105, 24, 212, 78, 173, 45, 0, 116, 226, 119,
        136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21, 130, 98, 241, 40, 154, 66, 184, 49,
        181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201, 164, 89, 216, 202, 220, 50,
        221, 152, 140, 33, 235, 214]


class ZhiHuEncrypt:
    headers = {
        'x-zse-93': x_zse_93,
        'x-api-version': '3.0.91',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-zse-96': '2.0_',
        'accept': '*/*',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_md5_code(un_str: str):
        return hashlib.md5(un_str.encode()).hexdigest()

    @staticmethod
    def get_ord_list(md5_code):
        return [ord(i) for i in md5_code]

    @staticmethod
    def get_Dv_48_list(c_v: list):
        return [int(127 * random.random()), 0] + c_v + [14 for _ in range(0, 14)]

    @staticmethod
    def get_Ev_Fv(d_v: list):
        return d_v[0:16], d_v[16:48]

    @staticmethod
    def get_Jv(e_v):
        return [e_v[i] ^ base_arr[i] ^ 42 for i in range(len(e_v))]

    @staticmethod
    def B_f(tt: list, te: int):
        return sls((255 & tt[te]), 24) | sls((255 & tt[te + 1]), 16) | sls((255 & tt[te + 2]), 8) | 255 & tt[te + 3]

    @staticmethod
    def G_f(tt: int):
        te = [0 for _ in range(0, 4)]
        tr = [0 for _ in range(0, 4)]
        ZhiHuEncrypt.i_f(tt, te, 0)
        # 下方的h_zb是一个固定的256位的数字数组
        tr[0] = h_zb[255 & te[0]]
        tr[1] = h_zb[255 & te[1]]
        tr[2] = h_zb[255 & te[2]]
        tr[3] = h_zb[255 & te[3]]
        ti = ZhiHuEncrypt.B_f(tr, 0)
        return ti ^ ZhiHuEncrypt.Q_f(ti, 2) ^ ZhiHuEncrypt.Q_f(ti, 10) ^ ZhiHuEncrypt.Q_f(ti, 18) ^ ZhiHuEncrypt.Q_f(ti,
                                                                                                                     24)

    @staticmethod
    def i_f(tt: int, te: list, tr: int):
        te[tr] = 255 & urs(tt, 24)
        te[tr + 1] = 255 & urs(tt, 16)
        te[tr + 2] = 255 & urs(tt, 8)
        te[tr + 3] = 255 & tt

    @staticmethod
    def Q_f(tt, te):
        return sls(band(4294967295, tt), te) | urs(tt, 32 - te)

    @staticmethod
    def __g_r(tt: list) -> list:
        te = [0 for _ in range(0, 16)]
        tr = [0 for _ in range(0, 36)]
        tr[0] = ZhiHuEncrypt.B_f(tt, 0)
        tr[1] = ZhiHuEncrypt.B_f(tt, 4)
        tr[2] = ZhiHuEncrypt.B_f(tt, 8)
        tr[3] = ZhiHuEncrypt.B_f(tt, 12)
        for i in range(0, 32):
            ta = ZhiHuEncrypt.G_f(tr[i + 1] ^ tr[i + 2] ^ tr[i + 3] ^ h_zk[i])  # 这里的h_zk同样也是一个固定的32位数组
            tr[i + 4] = tr[i] ^ ta
        ZhiHuEncrypt.i_f(tr[35], te, 0)
        ZhiHuEncrypt.i_f(tr[34], te, 4)
        ZhiHuEncrypt.i_f(tr[33], te, 8)
        ZhiHuEncrypt.i_f(tr[32], te, 12)
        return te

    @staticmethod
    def __g_x(tt: list, te: list) -> list:
        tr = []
        for i in range(0, 2):
            tu = tt[i * 16:(i + 1) * 16]  # 将32位数组切分，16个元素为一组
            tc = [None for _ in range(0, 16)]
            for j in range(0, 16):
                tc[j] = tu[j] ^ te[j]
            te = ZhiHuEncrypt.__g_r(tc)
            tr += te
        return tr

    @staticmethod
    def get_Mv(d_v):
        e_v, f_v = ZhiHuEncrypt.get_Ev_Fv(d_v)
        j_v = ZhiHuEncrypt.get_Jv(e_v)
        k_v = ZhiHuEncrypt.__g_r(j_v)
        l_v = ZhiHuEncrypt.__g_x(f_v, k_v)
        return k_v + l_v

    @staticmethod
    def final_encrypt(m_v):
        encrypt_str = ""
        for i in range(len(m_v) - 1, -1, -3):
            # 这里有四种算法，并且以4个为一组[0,24,16,8]这样循环。
            if i % 4 == 3:
                a_v = (m_v[i] ^ 58) + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            elif i % 4 == 0:
                a_v = m_v[i] + (sls(m_v[i - 1] ^ 58, 8)) + (sls(m_v[i - 2], 16))
            elif i % 4 == 1:
                a_v = m_v[i] + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2] ^ 58, 16))  # 此处M_v为基础逻辑中计算得出
            else:
                a_v = m_v[i] + (sls(m_v[i - 1], 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            # a_v = m_v[i] + (sls(m_v[i - 1] ^ 58, 8)) + (sls(m_v[i - 2], 16))  # 此处M_v为基础逻辑中计算得出
            b_v = a_v & 63
            encrypt_str += base_str[b_v]
            c_v = urs(a_v, 6) & 63
            encrypt_str += base_str[c_v]
            d_v = urs(a_v, 12) & 63
            encrypt_str += base_str[d_v]
            e_v = urs(a_v, 18)
            encrypt_str += base_str[e_v]
        return encrypt_str

    @staticmethod
    def encode(a_v):
        logger.warning("=====encrypt_begin=====")
        logger.info(f"a_v==>{a_v}")
        b_v = ZhiHuEncrypt.get_md5_code(a_v)
        logger.info(f"b_v==>{b_v}")
        c_v = ZhiHuEncrypt.get_ord_list(b_v)
        logger.info(f"c_v==>{c_v}")
        d_v = ZhiHuEncrypt.get_Dv_48_list(c_v)
        logger.info(f"d_v==>{d_v}")
        m_v = ZhiHuEncrypt.get_Mv(d_v)
        logger.info(f"m_v==>{m_v}")
        final_encrypt_code = ZhiHuEncrypt.final_encrypt(m_v)
        logger.info(f"final_encrypt_code==>{final_encrypt_code}")
        logger.warning("=====encrypt_end=====")
        return final_encrypt_code

    @staticmethod
    def get_d_c0():
        url_param = "/udid"
        a_v = ZhiHuEncrypt.encode(x_zse_93 + url_param)
        ZhiHuEncrypt.headers.update({"x-zse-96": '2.0_' + a_v})
        first_res = requests.post('https://www.zhihu.com/udid', data={}, headers=ZhiHuEncrypt.headers, timeout=10)
        cookie_t = requests.utils.dict_from_cookiejar(first_res.cookies)
        d_c0 = cookie_t.get('d_c0')
        logger.info(f"d_c0==> {d_c0}")
        return d_c0

    @staticmethod
    def get_result(url: str):
        url_host = "https://www.zhihu.com"
        url_path = url.split("?")[0].replace(url_host, "") + "?"
        url_params = url.split("?")[1]
        d_c0 = ZhiHuEncrypt.get_d_c0()
        a_v = x_zse_93 + "+" + url_path + url_params + "+" + d_c0
        encrypted_str = ZhiHuEncrypt.encode(a_v)
        ZhiHuEncrypt.headers.update({"x-zse-96": '2.0_' + encrypted_str})
        ZhiHuEncrypt.headers.update({"cookie": f"d_c0={d_c0};"})
        ZhiHuEncrypt.headers.update({'accept-encoding': 'gzip, deflate, br',
                                     'accept-language': 'zh-CN,zh;q=0.9'})
        res = requests.get(url, headers=ZhiHuEncrypt.headers, timeout=10)
        logger.info(f"final_result==>{res.json()}")
        return res.json()


if __name__ == '__main__':
    url = "https://www.zhihu.com/api/v4/members/lai-si-shuang-yu-27/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=220&limit=20"
    result = ZhiHuEncrypt.get_result(url)
    print(result)

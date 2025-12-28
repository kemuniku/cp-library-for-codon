#string for codon, PyPy3
class string:
    '''
    string for codon, PyPy3
    suffix array, LCP array, Z algorithmに対応しています。
    '''
    def _suffix_array(A: list[int]) -> list[int]:
        #Reference: https://qiita.com/flare/items/ac11972dbc590a91980d
        #Reference: https://speakerdeck.com/flare/sa-is
        if len(A) < 2:
            return list(range(len(A)))
        #Aを座標圧縮
        min_Ai, max_Ai = min(A), max(A)
        diff: int = max_Ai - min_Ai + 1
        if diff <= 5 * len(A):  #bucket sort
            bucket: list[int] = [0] * max(diff, len(A) + 1)
            for Ai in A:
                bucket[Ai - min_Ai] = 1
            mex: int = 1
            for x in range(diff):
                if bucket[x]:
                    bucket[x] = mex
                    mex += 1
            for i, Ai in enumerate(A):
                A[i] = bucket[Ai - min_Ai]
        else:  #O(NlogN) sort
            bucket: list[int] = sorted(range(len(A)), key = A.__getitem__)
            back: int = A[bucket[0]]
            mex: int = 1
            for i in bucket:
                if back != A[i]:
                    back: int = A[i]
                    mex += 1
                A[i] = mex
            mex += 1
            if mex > len(bucket):
                bucket.append(0)
        A.append(0)
        #SA-IS
        B: list[int] = [0] * len(A)
        R: list[int] = [0] * max(mex, len(A) >> 1)
        string._SAIS(A, B, bucket, R, mex)
        B.pop()
        return B
    def _SAIS(A: list[int], B: list[int], L: list[int], R: list[int], mex: int) -> None:
        #suffix-arrayの結果をB[-1:]に登録する
        #1. L, S, LMS typeの分類  T[i]: (L / S / LMS) = (-2, -1, 0から出現順採番)
        N: int = len(A)
        T: list[int] = [-1] * N
        LMS: list[int] = []
        for i in range(N - 2, -1, -1):
            T[i] = -2 if A[i] > A[i + 1] else T[i + 1] if A[i] == A[i + 1] else -1
        for i in range(1, N):
            if T[i - 1] == -2 and T[i] == -1:
                T[i] = len(LMS)
                LMS.append(i)
        #2. 頻度分布の作成  F[Ai]: -1 - indexedの累積和
        F: list[int] = [0] * (mex + 1)
        F[0] = -1
        for Ai in A:
            F[Ai + 1] += 1
        for Ai in range(mex):
            F[Ai + 1] += F[Ai]
        #3. induced sortを行い、LMS部分文字列を採番  C[i]: LMS[i]の採番結果
        string._induced_sort(A, B, L, R, F, T, LMS, mex)
        C: list[int] = [0] * len(LMS)
        same: bool = False
        if len(C) > 1:
            #a) B[0]以降最小のLMSを探す  -1 - indexedなので B[-1] = N - 1 に注意
            for i in range(N - 1):
                back: int = T[B[i]]
                if back >= 0:
                    C[back] = c = 1
                    Lback, Rback = LMS[back], LMS[back + 1]
                    break
            #b) LMS部分文字列を順に採番
            for i in range(i + 1, N - 1):
                now: int = T[B[i]]
                if now >= 0:  #A[Lback: Rback]  == A[Lnow: Rnow] の判定
                    Lnow, Rnow = LMS[now], LMS[now + 1]
                    if (Rback - Lback == Rnow - Lnow and
                        all(A[Lback + d] == A[Lnow + d] for d in range(Rback - Lback))):
                        same: bool = True
                        c -= 1  #一旦減算して次の行で補正
                    C[now] = c = c + 1
                    Lback, Rback, back = Lnow, Rnow, now
        #4. LMS orderを決め、再度induced sort
        if same == True:
            string._SAIS(C, B, L, R, c + 1)
            for x in range(-1, len(LMS) - 1):
                L[x + 1] = LMS[B[x]]  #x + 1の補正で-1 - indexedを修正
        else:
            for i, Ci in enumerate(C):
                L[Ci] = LMS[i]
        for i in range(len(LMS)):
            LMS[i] = L[i]
        string._induced_sort(A, B, L, R, F, T, LMS, mex)
    def _induced_sort(A: list[int], B: list[int], L: list[int], R: list[int],
                      F: list[int], T: list[int], LMS: list[int], mex: int) -> None:
        #1. 使い回す配列の初期化  [L[Ai], R[Ai]): 値AiのBへの挿入区間
        N: int = len(A)
        for Ai in range(mex):
            L[Ai], R[Ai] = F[Ai], F[Ai + 1]
        for i in range(-1, N - 1):
            B[i] = -1
        #2. LMS typeをバケット末尾から挿入
        for x in range(len(LMS) - 1, -1, -1):
            i: int = LMS[x]
            Ai: int = A[i]
            j = R[Ai] = R[Ai] - 1  #LMS[x]の挿入位置  assert B[j] == -1
            B[j] = i
        #3. L typeを先頭から挿入し、LMS typeを除去
        for x in range(-1, N - 1):
            i: int = B[x]
            if i > 0:  #挿入済み かつ i != 0
                if T[i - 1] == -2:
                    Aback: int = A[i - 1]  #assert B[L[Aback]] == -1
                    B[L[Aback]] = i - 1
                    L[Aback] += 1
                if T[i] >= 0:  #自身がLMS type
                    R[A[i]] += 1
                    B[x] = -1
        #4. S type, LMS typeを末尾から挿入
        for x in range(N - 2, -1, -1):
            i: int = B[x]
            if i > 0 and T[i - 1] != -2:
                Aback: int = A[i - 1]
                j = R[Aback] = R[Aback] - 1  #assert B[j] == -1
                B[j] = i - 1
        B[-1] = N - 1
    def _LCP(A, SA: list[int]) -> list[int]:
        N: int = len(A)
        LCP: list[int] = [0] * N
        rank: list[int] = [0] * N  #rank[i]: A[i:]のsuffix arrayの順位
        d: int = 0
        for x, SA_x in enumerate(SA):
            rank[SA_x] = x
        for i, rank_i in enumerate(rank):
            j: int = SA[rank_i - 1]
            while i + d < N > j + d and A[i + d] == A[j + d]:
                d += 1
            LCP[rank[j]] = d
            d = max(0, d - 1)
        if len(LCP) > 0:
            LCP[-1] = 0
        return LCP
    def _Z_algo(A) -> list[int]:
        #Reference: https://tjkendev.github.io/procon-library/python/string/z-algorithm.html
        N: int = len(A)
        B: list[int] = [0] * N
        if N > 0:
            B[0] = N
            Rt: int = 0
            same: int = 0
            ok: int = 0
            for i in range(1, N):
                if Rt:
                    Rt -= 1
                same += 1
                if B[same] < Rt:
                    B[i] = B[same]
                    continue
                while i + Rt < N and A[Rt] == A[i + Rt]:
                    Rt += 1
                B[i] = Rt
                same: int = 0
        return B
                
    #suffix array
    def suffix_array(S: str) -> list[int]:
        'N = len(S) として、O(N)でsuffix arrayを計算します。'
        return string._suffix_array([ord(Si) for Si in S])
    def suffix_array(S: list[str]) -> list[int]:
        return string._suffix_array([ord(Si) for Si in S])
    def suffix_array(A: list[int]) -> list[int]:
        '''
        N = len(A), d = max(A) - min(A) として、
        O(min(N + d, NlogN))でsuffix arrayを計算します。
        '''
        if len(A) == 0:
            return []
        elif isinstance(A[0], int):
            return string._suffix_array(A[:])
        else:  #Python・PyPy用分岐
            return string._suffix_array([ord(Ai) for Ai in A])

    #LCP array
    def LCP_array(A, SA: list[int]) -> list[int]:
        '''
        N = len(A), A: str | list[str] | list[int], SA = suffix_array(A) として、
        O(N)で長さNのLCP arrayを作成します。
        LCP[i]: 0 <= i < N - 1 のとき、A[SA[i]:]とA[SA[i + 1]:]の最長共通接頭辞
                i == N - 1 のとき、0
        '''
        assert len(A) == len(SA)
        return string._LCP(A, SA)

    #Z algorithm
    def Z_algorithm(A) -> list[int]:
        'すべての 0 <= i < N に対し、O(N)でAとA[i:]の最長共通接頭辞を求めます。'
        return string._Z_algo(A)

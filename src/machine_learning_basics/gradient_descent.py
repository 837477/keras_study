import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
diabetes = load_diabetes()

# 훈련 데이터 만들기
x = diabetes.data[:, 2]
y = diabetes.target

# - 예측값으로 올바른 모델 찾기
#############################################################################
# w와 b 초기화
w = 1.0
b = 1.0

# 훈련 데이터의 첫 번째 샘플 데이터로 y_hat 얻기
y_hat = x[0] * w + b

# 타깃과 예측 데이터 비교하기
print(y[0])
print(y_hat)
'''
출력 값
151.0
1.0616962065186886

현재 까지는 오차 범위가 매우 넓다는 것을 확인할 수 있다. 즉, 100% 오답을 예측했다고 판단할 수 있다.
그럼 다음 방법에서는 가중치(w)의 값을 조절하여 예측 값을 조금 더 조절해보자.
'''
#############################################################################

print("-" * 50)

# - 변화율를 통한 가중치 찾기
#############################################################################
# w 값을 조절해 예측 값 바꾸기
w_inc = w + 0.1
y_hat_inc = w_inc * x[0] + b
print(y[0])
print(y_hat_inc)
'''
출력 값
151.0
1.0678658271705574
미세하지만 이전의 1.0616962065186886 값에 비해서 조금 가까워진 결과를 얻을 수 있었다.
즉, w를 증가시킨 것은 올바른 결정이였다. (더 거리가 멀어지지 않고 타깃에 조금이라도 가까워 졌다.)
'''

# w값을 조정한 후 예측값 증가 정도 확인
w_rate = (y_hat_inc - y_hat) / (w_inc - w)
print(w_rate)
'''
y_hat_inc이나 y_hat은 결과적으로 x에 대한 식이다.
이를 다음과 같은 식으로 표현을 해보면,

w_rate = (y_hat_inc - y_hat) / (w_inc - w)
= (x[0] * w_inc + b) - (x[0] * w + b) / (w_inc - w)
= x[0] * ((w + 0.1) - w) / (w + 0.1) - w
= x[0]
즉, 변화율은 x[0] 그 자체이다.

그럼 만약 x[0] 이 변화율이 양수인지 음수인지에 따라서 w를 증가시킬 것인지 감소 시킬것인지 어떻게 판단할까?
그래프를 보면, 변화율이 양수 일 때, w를 증가하면 y_hat이 증가한다. (기울기가 양수 그래프)
반대로 변화율이 음수일 때, w이 감소하면 y_hay이 증가한다. (기울기가 음수 그래프)

그런데 w 값을 조절할 때 그냥 w_rate을 더해도될까?
기울기가 음수 그래프인 상태에서 w_rate를 구하게 된다면, 음수가 나오기 때문에 그대로 w_rate를 더해주면된다.
'''

# 변화율로 가중치 업데이트하기
w_new = w + w_rate
print(w_new)

# 변화율로 절편(b) 업데이트하기
b_inc = b + 0.1
y_hat_inc = x[0] * w + b_inc
print(y_hat_inc)
'''
b_rate = (y_hat_inc - y_hat) / (b_inc-b)
= (x[0] * w + b_inc) - (x[0] * w + b) / (b_inc - b)
= (b + 0.1) - b / (b + 0.1) - b
= 1
결과적으로 x[0~.. 무엇이든] 샢을을 이용해서 y_hat을 구하더라도 항상 b의 변화율은 1이된다.
b_new = b + 1
'''

# 절편 변화율 구하기
b_rate = (y_hat_inc - y_hat) / (b_inc - b)
print(b_rate)

b_new = b + 1
print(b_new)

'''
그런데 지금까지의 방식은 다음고 같은 문제가 있다.
- y_hat이 y에 한참 미치지 못 하는 값 인 경우, w와 b를 더 큰 폭으로 수정할 수 없다.
(앞에서 변화율 만큼 수정을 했지만 특별한 기준을 정하기 어려움)

- y_hat이 y보다 커지면 y_hat을 감소시키지 못한다.

따라서, y_hat과 y의 차이가 크면 w와 b를 그에 비례해서 바꿔야 하고, y_hat이 y보다 크면 w와 b를 감소시켜야한다. (능동적 대처)
'''
#############################################################################

print("-" * 50)

# - 오차 역전파로 더욱 더 적절한 가중치 찾기
#############################################################################
# 오차와 변화율을 곱하여 가중치 업데이트
err = y[0] - y_hat
w_new = w + w_rate * err
b_new = b + 1 * err
print(w_new, b_new)

'''
오차(err)를 구한다. 즉, y와 y_hat을 빼준 것
만약 타깃 값이 y > y_hat이면, 이 err는 아주 큰 양수 값이 될 것이고, 반대로 y < y_hat이면 음수 값이 된다.
따라서 w또한 이에 따라 능동적으로 바뀌게 된다.
'''

# 두 번째 샘플(x[1])을 사용하여 오차를 구하고 새로운 w와 b를 구하기
y_hat = x[1] * w_new + b_new
err = y[1] - y_hat
w_rate = x[1]
w_new = w_new + w_rate * err
b_new = b_new + 1 * err
print(w_new, b_new)
##############################################################################

print("-" * 50)

# - 전체 샘플을 통하여 가중치 찾기
#############################################################################
# 학습 데이터의 전체 샘플을 통한 학습 진행
for x_i, y_i in zip(x, y):
    y_hat = x_i * w + b
    err = y_i - y_hat
    w_rate = x_i
    w = w + w_rate * err
    b = b + 1 * err
print(w, b)

# 결과 출력 (산점도)
plt.scatter(x, y)
pt1 = (-0.1, -0.1 * w + b)
pt2 = (0.15, 0.15 * w + b)
plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]])
plt.xlabel('x')
plt.ylabel('y')
plt.show()
#############################################################################

print("-" * 50)

# - 에포크
#############################################################################
# 여러 에포크를 통한 반복 학습
for i in range(1, 100):
    for x_i, y_i in zip(x, y):
        y_hat = x_i * w + b
        err = y_i - y_hat
        w_rate = x_i
        w = w + w_rate * err
        b = b + 1 * err
print(w, b)

# 결과 출력
plt.scatter(x, y)
pt1 = (-0.1, -0.1 * w + b)
pt2 = (0.15, 0.15 * w + b)
plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]])
plt.xlabel('x')
plt.ylabel('y')
plt.show()
#############################################################################

print("-" * 50)

# - 학습된 모델로 값 예측하기
#############################################################################
x_new = 0.18
y_pred = x_new * w + b
print(y_pred)

plt.scatter(x, y)
plt.scatter(x_new, y_pred)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
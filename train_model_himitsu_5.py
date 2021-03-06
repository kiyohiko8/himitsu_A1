from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import random
import himitsu_data_gd_5
import numpy as np
import os
import gc
from sklearn.model_selection import KFold
#フォームによって収集した全データのインポート
import collected_himitsu_data_5
import collected_himitsu_sort


"""基本データの読み込み"""
#全ひみつ道具データの読み込み
himitsu  = himitsu_data_gd_5.mk_allword_list()
#ひみつ道具ベクトルの作成
word_vec = himitsu_data_gd_5.mk_vec(himitsu)


"""学習用データの整形"""
#収集したデータの読み込み
collected = collected_himitsu_data_5.read_csv("himitsu_data2.csv")
collected2 = collected_himitsu_data_5.read_csv("himitsu_data.csv")

#collected2の内容をcollectedに追加
for user in collected2:
	collected.append(user)

sorted = collected_himitsu_sort.count_sort(collected, himitsu)
#アンケートによって収集されたデータから知っている知識のみを収集
x_data = np.array(collected_himitsu_data_5.mk_x_train(himitsu, collected, sorted))
y_data = np.array(collected_himitsu_data_5.mk_y_train(himitsu, collected))

#訓練データの作成
#x_train, x_test, y_train, y_test =\
	#train_test_split(x_data, y_data, train_size = 0.8)
	


"""学習モデル構築"""

#パラメータの設定
epoch_num  = 50
batch_size = 10
in_num   = len(x_data[0]) #271
hidden_1 = 100
out_num  = len(y_data[0]) #271


#x_trainとy_trainの表示
print(collected)
print(x_data)
print(y_data)
print("len of x_train:", len(x_data))
print("len of y_train:", len(y_data))


#モデル構築,学習
model = Sequential()
model.add(Dense(input_dim = in_num, output_dim = hidden_1))
model.add(Activation("relu"))
#model.add(Dropout(0.5))

model.add(Dense(output_dim = out_num))
model.add(Activation("sigmoid"))

model.compile(loss="binary_crossentropy", optimizer=SGD(lr=0.1), metrics=['accuracy'])

"""交差検証"""

kf = KFold(n_splits=5, shuffle=True)
# 5回分のaccuracyの和を入れる(後で割る)
sum_accuracy = 0
# 5回分のaccuracyを1つ1つ保存する
accuracy = []
# 交差検証
for train_idx, val_idx in kf.split(X=x_data, y=y_data):
	train_x, val_x = x_data[train_idx], x_data[val_idx]
	train_t, val_t = y_data[train_idx], y_data[val_idx]
	#学習	
	history = model.fit(train_x, train_t, nb_epoch = epoch_num, batch_size=batch_size)
	#評価
	score = model.evaluate(val_x, val_t, verbose=0)
	acc = score[1]

	##評価値をリストに追加
	accuracy.append(acc)
	##今回の評価値を足す
	sum_accuracy += acc
print('accuracy : {}'.format(accuracy))
# 5回分の評価値の平均
sum_accuracy /= 5
print('Kfold accuracy: {}'.format(sum_accuracy))



"""
#モデル評価
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#テストデータと結果の表示
predictions = model.predict(x_test)
correct = y_test
print("x_test:")
print(x_test[0])
print("predictions:")
print(predictions[0])
print("correct:")
print(correct[0])
"""

#モデルの保存
print("Saving Model...")
json_string = model.to_json()
a = input("input file number:")
open('predict_model_himitsu_'+str(a)+'.json', 'w').write(json_string)
print("Saved!")

#パラメータの保存
print("Saving Param...")
b = input("input file number:")
model.save_weights('predict_weights_himitsu_'+str(b)+'.h5')
print("Saved!")

gc.collect()












	




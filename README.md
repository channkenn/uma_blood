# uma_blood

uma の血統表を見える化する

1.csv/bloodline_netkeiba5_cfm.csv を組み立てる
2.scripts/blood_all_netkeiba5_cfm_f.py を実行するとウマ娘のサイアーラインが生成される。svg/uma_blood_netkeiba5_cfm_f.svg
3.bloodline_netkeiba5.csv を組み立てる。これは netkeiba でブックマークレットを動かす
4.scripts/netkeiba5.py を実行すると 3.から格ウマ個別の５代血統図が svg/に生成される

画像の処理 1.ウマ娘から 400px のオリジナル画像をダウンロードして img/org に入れる
2.resize_images.py を実行する。img/100px にリサイズされたウマ娘画像が入る
3.img_sequence.py を実行する。img/に csv/bloodline.csv で定義された数字が付与されウマ娘画像が入る。

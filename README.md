# uma_blood

uma の血統表を見える化する（事前に画像処理をすること)
1.bloodline_netkeiba5.csv を netkeiba の血統表からブックマークレットを使って生成する。
2.scripts/netkeiba5.py を実行すると ウマ個別の５代血統図が svg/に、bloodline_netkeiba5_cfm.csv が csv/に生成される。
3.scripts/blood_all_netkeiba5_cfm_f.py を実行するとウマ娘のサイアーラインが生成される。svg/uma_blood_netkeiba5_cfm_f.svg
4.scripts/imagepath_replace.py を実行して SVG ファイル内の img パスを github 上の img へ置き換える

画像の処理 1.ウマ娘から 400px のオリジナル画像をダウンロードして img/org に入れる
2.resize_images.py を実行する。img/100px にリサイズされたウマ娘画像が入る
3.img_sequence.py を実行する。img/seq に csv/bloodline.csv で定義された数字が付与されウマ娘画像が入る。
4.rename_images.py を実行する。img/にローマ字化した数字付 100px ウマ娘画像が生成される。

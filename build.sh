pip3 install -r requirements.txt
now=$(date)
python3 runner.py 2>&1 | tee build.log

rm -rf build/*.json build/*.log build/*.date

cp providers.json build/
cp servers.json build/
cp build.log build/
echo "$now" > build/build.date
echo "Build complete"
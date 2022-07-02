screenid=$(ps aux | grep epd | awk -F '${epd}' '{print $1}' | awk  '{print $2}' | awk '{print $1}' | sed -n 1p |cut -d " " -f1); sudo kill $screenid

kill $(ps aux | grep Rl+ | grep receiver.py | awk '{print $2}')
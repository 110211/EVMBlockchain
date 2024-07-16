# Biến toàn cục để lưu trữ thông tin giám sát
from collections import defaultdict

from flask import request

import blockchain


monitoring_info = {
    'total_blocks': 0,
    'total_transactions': 0,
    'node_performance': defaultdict(list)  # Lưu trữ thời gian xử lý giao dịch của mỗi node
}

def update_monitoring_info(algorithm, start_time, end_time):
    monitoring_info['total_blocks'] += 1
    monitoring_info['total_transactions'] += len(blockchain[-1].transactions)
    monitoring_info['node_performance'][request.remote_addr].append(end_time - start_time)

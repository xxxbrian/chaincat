from src.jobs.transfers_volume import *


def run_jobs() -> dict:
    job1=transfers_volume()
    vl = job1['24h volume']
    msg = f'Today transfers volume is {vl}.'
    resp = {
        'status':job1['status'],
        'msg': msg,
    }
    return resp


if __name__ == '__main__':
    print(run_jobs())
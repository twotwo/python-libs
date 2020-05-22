import io
import os
import tarfile

import multiprocessing as mp

mp.set_start_method("spawn", True)

test_file = "./test.tar"


def test_decrypt():
    reader, proc = get_reader(test_file)
    with os.fdopen(reader, "rb", buffering=4096) as fr:
        # load data to memory
        byte_array = io.BytesIO(fr.read())
    try:
        fr.close()
        proc.terminate()
    except Exception:
        pass
    tf = tarfile.open(fileobj=byte_array, mode="r|*", encoding="utf8")
    print(f"test_decrypt, pid={mp.current_process().pid}, {tf.getnames()}")


def _decrypt(model_path: str, write_pipe: mp.Pipe):
    """decrypt model to mp.Pipe()
    """
    print("Transfer Data ...")
    f = os.fdopen(write_pipe.fileno(), "wb")
    with open(model_path, "rb") as tar:
        data = tar.read()
        f.write(data)
    return


def get_reader(model_path: str):
    r, w = mp.Pipe(False)
    proc = mp.Process(target=_decrypt, args=(model_path, w))
    proc.start()
    reader = os.dup(r.fileno())

    return reader, proc


if __name__ == "__main__":
    test_decrypt()

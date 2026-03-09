# 无损压缩算法
import zlib
import base64

class LosslessCompression:
    @staticmethod
    def compress(data, level=9):
        """压缩数据"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        compressed = zlib.compress(data, level)
        return base64.b64encode(compressed).decode('utf-8')
    
    @staticmethod
    def decompress(compressed_data):
        """解压缩数据"""
        compressed = base64.b64decode(compressed_data)
        decompressed = zlib.decompress(compressed)
        return decompressed.decode('utf-8')
    
    @staticmethod
    def compress_file(file_path, output_path):
        """压缩文件"""
        with open(file_path, 'rb') as f:
            data = f.read()
        compressed = zlib.compress(data)
        with open(output_path, 'wb') as f:
            f.write(compressed)
    
    @staticmethod
    def decompress_file(compressed_path, output_path):
        """解压文件"""
        with open(compressed_path, 'rb') as f:
            compressed = f.read()
        decompressed = zlib.decompress(compressed)
        with open(output_path, 'wb') as f:
            f.write(decompressed)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子书网站爬虫示例
仅用于获取公开的图书元数据，请确保遵守网站使用条款和版权法律
"""

import requests
import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ElectronicBookSpider:
    """电子书爬虫类"""
    
    def __init__(self, base_url="https://findxsyu.libsp.cn/#/elecBook"):
        self.base_url = base_url
        self.session = requests.Session()
        self.driver = None
        self.books_data = []
        
        # 设置请求头，模拟真实浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        self.session.headers.update(self.headers)
    
    def setup_driver(self):
        """设置 Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("WebDriver 初始化成功")
        except Exception as e:
            logger.error(f"WebDriver 初始化失败: {e}")
            return False
        return True
    
    def get_page_with_selenium(self, url, wait_time=10):
        """使用 Selenium 获取动态加载的页面内容"""
        try:
            self.driver.get(url)
            # 等待页面加载完成
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 获取页面源码
            page_source = self.driver.page_source
            return page_source
        except Exception as e:
            logger.error(f"获取页面失败: {e}")
            return None
    
    def parse_book_list(self, html_content):
        """解析图书列表页面"""
        soup = BeautifulSoup(html_content, 'html.parser')
        books = []
        
        # 这里需要根据实际网站结构调整选择器
        # 以下是示例选择器，需要根据实际网站修改
        book_elements = soup.find_all('div', class_='book-item')  # 示例选择器
        
        for book_element in book_elements:
            try:
                book_data = {
                    'title': self.extract_text(book_element, '.book-title'),
                    'author': self.extract_text(book_element, '.book-author'),
                    'publisher': self.extract_text(book_element, '.book-publisher'),
                    'isbn': self.extract_text(book_element, '.book-isbn'),
                    'description': self.extract_text(book_element, '.book-description'),
                    'category': self.extract_text(book_element, '.book-category'),
                    'cover_url': self.extract_attribute(book_element, '.book-cover img', 'src'),
                    'detail_url': self.extract_attribute(book_element, 'a', 'href'),
                }
                books.append(book_data)
                logger.info(f"解析图书: {book_data.get('title', 'Unknown')}")
            except Exception as e:
                logger.error(f"解析图书元素失败: {e}")
                continue
        
        return books
    
    def extract_text(self, element, selector):
        """提取文本内容"""
        try:
            found = element.select_one(selector)
            return found.get_text(strip=True) if found else ""
        except:
            return ""
    
    def extract_attribute(self, element, selector, attribute):
        """提取属性值"""
        try:
            found = element.select_one(selector)
            return found.get(attribute, "") if found else ""
        except:
            return ""
    
    def search_books(self, keyword="", category="", page=1):
        """搜索图书"""
        logger.info(f"搜索图书 - 关键词: {keyword}, 分类: {category}, 页码: {page}")
        
        # 构建搜索 URL（需要根据实际网站 API 调整）
        search_url = f"{self.base_url}?keyword={keyword}&category={category}&page={page}"
        
        # 获取页面内容
        html_content = self.get_page_with_selenium(search_url)
        if not html_content:
            return []
        
        # 解析图书列表
        books = self.parse_book_list(html_content)
        return books
    
    def get_book_detail(self, book_url):
        """获取图书详细信息"""
        logger.info(f"获取图书详情: {book_url}")
        
        html_content = self.get_page_with_selenium(book_url)
        if not html_content:
            return {}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 解析详细信息（需要根据实际网站结构调整）
        detail_data = {
            'title': self.extract_text(soup, '.detail-title'),
            'author': self.extract_text(soup, '.detail-author'),
            'publisher': self.extract_text(soup, '.detail-publisher'),
            'isbn': self.extract_text(soup, '.detail-isbn'),
            'publish_date': self.extract_text(soup, '.detail-publish-date'),
            'pages': self.extract_text(soup, '.detail-pages'),
            'language': self.extract_text(soup, '.detail-language'),
            'description': self.extract_text(soup, '.detail-description'),
            'table_of_contents': self.extract_text(soup, '.detail-toc'),
            'cover_image': self.extract_attribute(soup, '.detail-cover img', 'src'),
        }
        
        return detail_data
    
    def save_to_json(self, filename="books_data.json"):
        """保存数据到 JSON 文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.books_data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存 JSON 文件失败: {e}")
    
    def save_to_csv(self, filename="books_data.csv"):
        """保存数据到 CSV 文件"""
        try:
            if not self.books_data:
                logger.warning("没有数据可保存")
                return
            
            fieldnames = self.books_data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.books_data)
            logger.info(f"数据已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存 CSV 文件失败: {e}")
    
    def crawl_with_delay(self, max_pages=10, delay=2):
        """带延迟的爬取，避免对服务器造成压力"""
        logger.info("开始爬取图书数据...")
        
        for page in range(1, max_pages + 1):
            logger.info(f"正在爬取第 {page} 页...")
            
            # 搜索图书
            books = self.search_books(page=page)
            if not books:
                logger.info(f"第 {page} 页没有找到图书，停止爬取")
                break
            
            # 获取每本书的详细信息
            for book in books:
                if book.get('detail_url'):
                    detail = self.get_book_detail(book['detail_url'])
                    book.update(detail)
                
                self.books_data.append(book)
                
                # 添加延迟，避免请求过于频繁
                time.sleep(delay)
            
            logger.info(f"第 {page} 页完成，已获取 {len(books)} 本图书")
            
            # 页面间延迟
            time.sleep(delay * 2)
    
    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver 已关闭")
        
        if self.session:
            self.session.close()
            logger.info("Session 已关闭")

def main():
    """主函数"""
    spider = ElectronicBookSpider()
    
    try:
        # 初始化 WebDriver
        if not spider.setup_driver():
            logger.error("无法初始化 WebDriver，程序退出")
            return
        
        # 开始爬取
        spider.crawl_with_delay(max_pages=5, delay=3)
        
        # 保存数据
        spider.save_to_json()
        spider.save_to_csv()
        
        logger.info(f"爬取完成，共获取 {len(spider.books_data)} 本图书信息")
        
    except KeyboardInterrupt:
        logger.info("用户中断爬取")
    except Exception as e:
        logger.error(f"爬取过程中发生错误: {e}")
    finally:
        spider.close()

if __name__ == "__main__":
    main() 
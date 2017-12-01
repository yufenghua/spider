#!/usr/bin/env python
# -*- coding: utf-8 -*-
aa=response.xpath('//body//div[@class="page-box fr"]').extract_first()

soup = BeautifulSoup(response.body,"lxml")


#!/usr/bin/python
#coding: utf8
#########################################################################
# File Name: consts.py
# Author: Justin Leo Ye
# Mail: justinleoye@gmail.com 
# Created Time: Tue Nov 17 13:46:30 2015
#########################################################################


DEFECT_CLAS_LIST = ['type', 'serverity', 'priority', 'status', 'origin', 'source', 'root_cause']

DEFECT_CLASSIFICATIONS = {
    "type": {
        "name": ("defect_type", u"缺陷类型"),
        "classification": [("function", u"Function--影响了重要的特性、用户界面、产品接口、硬件结构接口和全局数据结构。并且设计文档需要正式的变更。如逻辑,指针,循环,递归,功能等缺陷。"), ("assignment", u"Assignment--需要修改少量代码,如初始化或控制块。如声明、重复命名,范围、限定等缺陷。"), ("interface", u"Interface--与其他组件、模块或设备驱动程序、调用参数、控制块或参数列表相互影响的缺陷。"), ("checking", u"Checking--提示的错误信息,不适当的数据验证等缺陷。"), ("build_package_merge", u"Build/Package/Merge--由于配置库、变更管理或版本控制引起的错误。"), ("documentation", u"Documentation--影响发布和维护,包括注释。"), ("algorithm", u"Algorithm--算法错误。"), ("user_interface", u"User Interface--人机交互特性:屏幕格式,确认用户输入,功能有效性,页面排版等方面的缺陷。"), ("performance", u"Performance--不满足系统可测量的属性值,如:执行时间,事务处理速率等。"), ("norms", u"Norms--不符合各种标准的要求,如编码标准、设计符号等。")]
    },
    "serverity": {
        "name": ("defect_serverity", u"缺陷严重程度"),
        "classification": [("critical", u"不能执行正常工作功能或重要功能。或者危及人身安全"), ("major", u"严重地影响系统要求或基本功能的实现,且没有办法更正"), ("minor", u"严重地影响系统要求或基本功能的实现,但存在合理的更正办法"), ("cosmetic", u"使操作者不方便或遇到麻烦,但它不影响执行工作功能或重要功能"), ("other", u"其它错误")]
    },
    "priority": {
        "name": ("defect_prioriry", u"缺陷优先级"),
        "classification": [("resolve_immediately", u"缺陷必须立即被解决"), ("normal_queue", u"缺陷需要正常排队等待被修复"), ("not_urgent", u"缺陷可以在方便时被修复")]
    },
    "status": {
        "name": ("defect_status", u"缺陷状态"),
        "classification": [("submitted", u"已提交"), ("open", u"确认的“提交的缺陷”，待处理"), ("rejected", u"否决的“提交的缺陷”，不需要修复或者不是缺陷"), ("resolved", u"缺陷被修复"), ("closed", u"确认被修复的缺陷，将其关闭")]
    },
    "origin": {
        "name": ("defect_origin", u"缺陷起源"),
        "classification": [("requirement", u"在需求阶段发现的缺陷"), ("architecture", u"在架构阶段发现的缺陷"), ("design", u"在设计阶段发现的缺陷"), ("code", u"在编码阶段发现的缺陷"), ("test", u"在测试阶段发现的缺陷")]
    },
    "source": {
        "name": ("defect_source", u"缺陷来源"),
        "classification": [("requirement", u"由于需求问题引起的缺陷"), ("architecture", u"由于架构问题引起的缺陷"), ("design", u"由于设计问题引起的缺陷"), ("code", u"由于编码问题引起的缺陷"), ("test", u"由于测试问题引起的缺陷"), ("integration", u"由于集成问题引起的缺陷")]
    },
    "root_cause": {
        "name": ("defect_root_cause", u"缺陷根源"),
        "classification": [("target", u"目标"), ("process_tool_method", u"过程、工具或方法"), ("people", u"人"), ("orgnization_communication", u"缺乏组织和通信"), ("hardware", u"硬件"), ("software", u"软件"), ("environment", u"环境")]
    }
}




import sdtp_db.model as bd
import backend.services as df
import backend.DynamicCalculation as dc
import crud as crud
run = True
session = bd.Session()

# while(run):
#     s = '='
    # print()
    # print("> Static and Dynamic Testes Pile <")
    # print(s*20)
    # print("[1] Типы свай")
    # print("[2] Производители")
    # print("[3] Испытанные сваи")
    # print("[4] Все испытания")
    # print("[5] Забивка")
    # print("[6] Добивка")
    # print("[7] Расчет\n ---------")
    # print("[0] выход")
    # print(s*20)
    # print()
    # action = input()
    # input("Введите действие: ")


#
# print(*df.get_element(session,bd.BuildObject), sep ='\n')
# print(*df.get_element(session, bd.DynamicTested))
print(round(dc.calculate_bearing_capacity(1,1,1),2))
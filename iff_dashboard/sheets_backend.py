import pandas as pd
from gsheets_utils import random_with_N_digits, get_spreadsheet
from db_utils import insert_to_tech_partners, insert_to_location
from gspread import Cell
from frt import Frt
from config import ACCEPT_MESSAGE, REJECT_MESSAGE, SUBMIT_MESSAGE


def update_frts(spreadsheet):
    frt_sheet = spreadsheet.get_worksheet(0)
    update_list = frt_sheet.col_values(6)
    print(update_list)
    gs_cells = []
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            values_list = frt_sheet.row_values(i)
            frt = Frt(*values_list)
            frt.insert_to_frt_table()
            frt.update_frt_place_table()
            gs_cells.append(Cell(i, 1, value=frt.id))
            gs_cells.append(Cell(i, 6, value=ACCEPT_MESSAGE))

    if gs_cells:
        frt_sheet.update_cells(gs_cells)


def update_tech_partner(spreadsheet):
    tp_sheet = spreadsheet.get_worksheet(1)
    update_list = tp_sheet.col_values(4)
    gs_cells = []
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            values_list = tp_sheet.row_values(i)
            if values_list[0] == '':
                uuid = random_with_N_digits(6)
                gs_cells.append(Cell(i, 1, value=uuid))
                values_list[0] = uuid

            insert_to_tech_partners(
                values_list[0], values_list[1], values_list[2])
            gs_cells.append(Cell(i, 4, value=ACCEPT_MESSAGE))

    if gs_cells:
        tp_sheet.update_cells(gs_cells)


def update_location_table(spreadsheet):
    location = spreadsheet.get_worksheet(2)
    update_list = location.col_values(1)
    update_list = update_list[1:]
    i = 0
    for state in update_list:
        i += 1
        insert_to_location(i, state)


if __name__ == '__main__':
    spreadsheet = get_spreadsheet()
    print('updating tech partners')
    update_tech_partner(spreadsheet)
    # update_location_table(spreadsheet)
    print('updating frt sheet')
    update_frts(spreadsheet)

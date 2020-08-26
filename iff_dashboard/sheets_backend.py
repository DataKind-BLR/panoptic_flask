from config import ACCEPT_MESSAGE, REJECT_MESSAGE, SUBMIT_MESSAGE
from frt import Frt
from gsheets_utils import get_spreadsheet
from gspread import Cell
from location import Location
from tech_partner import TechPartner


def update_frts(spreadsheet):
    frt_sheet = spreadsheet.get_worksheet(0)
    update_list = frt_sheet.col_values(7)
    gs_cells = []
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            values_list = frt_sheet.row_values(i)
            frt = Frt(*values_list)
            frt.insert_to_frt_table()
            frt.update_frt_place_table()
            frt.add_rti_replies()
            frt.add_govt_link()
            frt.add_media_link()
    #         gs_cells.append(Cell(i, 1, value=frt.id))
    #         gs_cells.append(Cell(i, 6, value=ACCEPT_MESSAGE))

    # if gs_cells:
    #     frt_sheet.update_cells(gs_cells)


def update_tech_partner(spreadsheet):
    tp_sheet = spreadsheet.get_worksheet(1)
    update_list = tp_sheet.col_values(5)
    gs_cells = []
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            values_list = tp_sheet.row_values(i)
            tech_partner = TechPartner(*values_list)
            tech_partner.insert_to_tech_partners()
    #         gs_cells.append(Cell(i, 1, value=tech_partner.id))
    #         gs_cells.append(Cell(i, 4, value=ACCEPT_MESSAGE))

    # if gs_cells:
    #     tp_sheet.update_cells(gs_cells)


def update_location_table(spreadsheet):
    location = spreadsheet.get_worksheet(2)
    update_list = location.col_values(1)
    update_list = update_list[1:]
    for _id, state in enumerate(update_list, 1):
        location = Location(_id, state)
        location.insert_to_location()


if __name__ == '__main__':
    spreadsheet = get_spreadsheet()
    print('updating tech partners')
    update_tech_partner(spreadsheet)
    update_location_table(spreadsheet)
    print('updating frt sheet')
    update_frts(spreadsheet)

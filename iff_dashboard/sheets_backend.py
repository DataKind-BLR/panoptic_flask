from config import ACCEPT_MESSAGE, REJECT_MESSAGE, SUBMIT_MESSAGE, DELETE_MESSAGE
from frt import Frt
from gsheets_utils import get_spreadsheet
from gspread import Cell
from location import Location
from tech_partner import TechPartner


def update_frts(spreadsheet):
    '''
    This method is used to push the changes from the frt spreadsheet to the database.
    It includes addition, updation and deletion of data.
    :spreadsheet object: the access to google spreadsheet.

    '''
    # Read the frt sheet and make a update list.
    frt_sheet = spreadsheet.get_worksheet(0) 
    update_list = frt_sheet.col_values(7)
    gs_cells = []
    delete_rows =[]
    print('read sheet')
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            try:
                values_list = frt_sheet.row_values(i)
                frt = Frt(*values_list)
                frt.insert_to_frt_table()
                frt.update_frt_place_table()
                frt.add_rti_replies()
                frt.add_govt_link()
                frt.add_media_link()
                # Acknowledge the database updation on the spreadsheet.
                gs_cells.append(Cell(i, 1, value=frt.id))
                gs_cells.append(Cell(i, 7, value=ACCEPT_MESSAGE))
            except:
                gs_cells.append(Cell(i, 7, value=REJECT_MESSAGE))
        
        if update_status == DELETE_MESSAGE:
            values_list = frt_sheet.row_values(i)
            frt = Frt(*values_list)
            frt.delete_frt()
            delete_rows.append(i)

    delete_rows.reverse()
    for i in delete_rows:
        frt_sheet.delete_rows(i)

    if gs_cells:
        frt_sheet.update_cells(gs_cells)


def update_tech_partner(spreadsheet):
    '''
    This method is used to push the changes from the tech_partners spreadsheet to the database.
    It includes addition, updation and deletion of data.
    :spreadsheet object: the access to google spreadsheet.

    '''
    tp_sheet = spreadsheet.get_worksheet(1)
    print('read sheet')
    update_list = tp_sheet.col_values(5)
    gs_cells = []
    for i, update_status in enumerate(update_list, 1):
        if update_status == SUBMIT_MESSAGE:
            values_list = tp_sheet.row_values(i)
            tech_partner = TechPartner(*values_list)
            tech_partner.insert_to_tech_partners()
            gs_cells.append(Cell(i, 1, value=tech_partner.id))
            gs_cells.append(Cell(i, 5, value=ACCEPT_MESSAGE))

    if gs_cells:
        tp_sheet.update_cells(gs_cells)


def update_location_table(spreadsheet):
    '''
    This method is used to push the changes from the location spreadsheet to the database.
    It includes addition, updation and deletion of data.
    :spreadsheet object: the access to google spreadsheet.

    '''
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

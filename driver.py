from ptcl_dbill import PTCL_dbill

def main():
    """Driver function to download the bill."""
    obj = PTCL_dbill()
    obj.fill_dbill_form()
    obj.save_dbill(path="./")

if __name__ == '__main__':
    main()
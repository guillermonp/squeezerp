"""
Qt stylesheets
"""

DATATOOLS_GLOBAL = """

    QScrollBar:vertical, QScrollBar:horizontal {
        border: none;
        background: #e67e22;
        width: 10px;
    }
    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: #e67e22;
        min-height: 1px;
    }

    QComboBox {
        border: 1px #e67e22;
        padding: 1px 18px 1px 3px;
        min-width: 6em;
        color: white;
        background-color: #e67e22;
        margin: 0 0 0 0;
    }

    QComboBox:on {
        padding-top: 3px;
        padding-left: 4px;
        background-color:  #e67e22;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 15px;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
        background-color: #f39c12;
    }

    QComboBox::down-arrow {
        image: url(imgs/cbo_arrow.png);
        height: 10px;
    }

    QComboBox QAbstractItemView {
        background: #ecf0f1;
        selection-background-color: #e67e22;
    }
    """

PROGRESS_BAR = """
    QProgressBar::chunk {
    background-color: #e67e22;
    width: 200px;
    }

    QProgressBar {
        border: 1px solid #d35400;
        text-align: center;
    }"""

PUSH_BUTTON = """
    QPushButton {
        background-color:#e67e22;
        border-style: outset;
        border: 1px solid #e67e22;
        color: white;
    }
    QPushButton:hover {
        background-color:#f39c12;
        border-style: outset;
        border: 1px solid #f39c12;
    }

    QPushButton:pressed {
        background-color:#d35400;
        border-style: outset;
        border: 1px solid #d35400;
    }"""

CSV_BUTTON = """
    QToolButton {
        background:transparent;
        border:none;
    }

    QToolButton:checked#csv_button, QToolButton:pressed#csv_button {
        background:rgb(242, 210, 255);
        border:1px solid rgb(242, 210, 255);
    }

    QToolButton:hover#csv_button{
        background-color: rgb(242, 210, 255)}
"""

XLS_BUTTON = """
    QToolButton {
        background:transparent;
        border:none;
    }

    QToolButton:checked#xls_button, QToolButton:pressed#xls_button {
        background:rgb(196, 255, 210);
        border:1px solid rgb(196, 255, 210);
    }

    QToolButton:hover#xls_button{
        background-color: rgb(196, 255, 210);}
"""

DATATOOLS_ERROR_TABLE = """background-color: rgb(242, 220, 219);"""
DATATOOLS_PASS_TABLE = """background-color: rgb(183, 255, 183);"""
from modules.models import Basic, Custom, Sample, InvoiceJson


def test_invoice_json_creation():
    # 有効なデータでInvoiceJsonインスタンスを作成
    invoice_json = InvoiceJson(
        datasetId="1s1199df4-0d1v-41b0-1dea-23bf4dh09g12",
        basic=Basic(
            dateSubmitted=None,
            dataOwnerId="0c233ef274f28e611de4074638b4dc43e737ab993132343532343430",
            dataName="test-scatter-plot-dataset",
            instrumentId=None,
            experimentId=None,
            description=None,
        ),
        custom=Custom(
            measurement_data_start_character="Data",
            x_axis_column_index=1,
            y_axis_column_index=2,
            xaxis_label_name="test-xラベル",
            yaxis_label_name="test-yラベル",
            key1=None,
            key2=None,
            key3=None,
            key4=None,
            key5=None,
            key6=None,
            key7=None,
            key8=None,
            key9=None,
            key10=None,
        ),
        sample=Sample(
            sampleId=None,
            names=["test1"],
            composition=None,
            referenceUrl=None,
            description=None,
            generalAttributes=[],
            ownerId="de17c7b3f0ff5126831c2d519f481055ba466ddb6238666132316439",
        ),
    )

    assert invoice_json.get_xaxis_label_name() == "test-xラベル"
    assert invoice_json.get_yaxis_label_name() == "test-yラベル"

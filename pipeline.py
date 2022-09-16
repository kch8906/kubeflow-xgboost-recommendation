import os

import kfp
import kfp.components as comp
from kfp import dsl
from kfp import onprem


@dsl.pipeline(
    name="xgboost pipeline",
    description="xgboost pipeline"
)
def xgboost_pipeline():

    data_vop = dsl.VolumeOp(
            name="data-volume",
            resource_name="data-pvc",
            modes=dsl.VOLUME_MODE_RWO,
            size="5Gi"
        )

    data_0 = dsl.ContainerOp(
            name="load & preprocess data pipeline",
            image="byeongjokim/mnist-pre-data:latest",
        ).set_display_name('collect & preprocess data')\
        .apply(onprem.mount_pvc("data-pvc", volume_name="data", volume_mount_path="/data"))
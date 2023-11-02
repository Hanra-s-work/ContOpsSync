#:/bin/bash
echo Removing all the pods that have the Failed status
echo "Running: sudo kubectl delete pods --selector=run=broken --field-selector=status.phase=Failed"
sudo kubectl delete pods --selector=run=broken --field-selector=status.phase=Failed

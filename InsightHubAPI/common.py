from rest_framework.response import Response
from rest_framework import status

def commonPostApi(serializer):
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def commonDeleteApi(model_name, id):
    try:
        obj = model_name.objects.get(pk=id, isDeleted=False)
        obj.isDeleted = True
        try:
            obj.save()
            return Response({"message": "Successfully deleted.", "success": True}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Some error occured.", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({"message": "Invalid Data.", "success": False}, status=status.HTTP_400_BAD_REQUEST)
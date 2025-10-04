from django.http import HttpResponse
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from mbamain.models import  Signature
from mbamain.utils.shortcuts import require_auth
from mbamain.models import Cv
from django.http import HttpResponseNotFound, HttpResponseServerError

@require_auth
def upload_signature(request):
    if request.method == "POST":
        try:
            signature = request.FILES["signature"]
            if request.user.has_signature:
                # If the user already has a signature, then send a error message since as signature can only be uploaded once
                messages.error(request, "You have already uploaded a signature. You cannot upload another one.")
                return redirect("mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile")

            sig = Signature(
                user=request.user,
                img_path = signature
                )
            sig.save()
            request.user.has_signature = True
            request.user.save()
            messages.success(request, "Signature uploaded successfully.")
        except KeyError:
            messages.error(request, "No signature file provided.")
        except Exception as e:
            messages.error(request, f"An error occurred while uploading the signature - {str(e)}")

    url = "mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile"
    return redirect(url)


@require_auth
def upload_cv(request):
    if request.method == "POST":
        try:
            cv_file = request.FILES["cv"] 
            if not cv_file.name.endswith('.pdf'):
                messages.error(request, "CV must be a PDF file.")
                return redirect("mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile")
            if request.user.has_cv:
                cv = request.user.cv
                cv.cv_file.delete()
                cv.delete()
            # If the user already has a CV, delete the old one before saving the new one

            cv = Cv(
                user=request.user,
                cv_file=cv_file
            )
            cv.save()
            request.user.has_cv = True
            request.user.save()
            messages.success(request, "CV uploaded successfully.")
        except KeyError:
            messages.error(request, "No CV file provided.")
        except Exception as e:
            messages.error(request, f"An error occurred while uploading the CV - {str(e)}")

    url = "mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile"
    return redirect(url)



@require_auth
def download_cv(request):
    if request.method == "GET":
        try: 
            cv_id = request.GET.get("id")
            cv = get_object_or_404(Cv, pk=cv_id).cv_file
            file_path = cv.path
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{cv.name}"'
                return response
        except Exception as e:
            messages.error(request, f"An error occurred while downloading the CV - {str(e)}")
            return redirect("mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile")


@require_auth
def load_signature(request, id): # gets the signature by id
    if request.method == "GET":
        sig = get_object_or_404(Signature, pk=id).img_path
        file_path = sig.path
        try:
           with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/*')
            response['Content-Disposition'] = f'attachment; filename="{sig.name}"'
            return response
        except:
         return HttpResponseServerError()
    return HttpResponseNotFound()


@require_auth
def download_signature(request): #downloads a user's signature
  if request.method== "GET":
    try:
      signature = request.user.signature.img_path
      file_path = signature.path
      with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='image/*')
        response['Content-Disposition'] = f'attachment; filename="{signature.name}"'
        return response
    except:
      messages.error(request, f"An error occurred while downloading the signature ")
      return redirect("mba_main:profile_scholar" if request.user.is_scholar() else "mba_main:profile")
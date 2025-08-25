# accident_project/views.py (최종)

from datetime import datetime
import json, re
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from .constants import LABEL_COLORS, PART_ANCHORS
from .models import AccidentRecord, Agreement

# 서버측 단순 PDF Fallback
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ---------------------------
# 공통 유틸
# ---------------------------
def _get_agreement_payload_or_404(pk: int):
    rec = get_object_or_404(Agreement, pk=pk)
    try:
        payload = json.loads(rec.damages_raw or "{}")
    except json.JSONDecodeError:
        payload = {}
    return rec, payload


def mask_rrn_value(v: str) -> str:
    if not v:
        return v
    m = re.match(r"^(\d{6})-(\d)(\d{6})$", v)
    return f"{m.group(1)}-{m.group(2)}******" if m else v


def _fmt_k(dtstr: str) -> str:
    """YYYY-MM-DD HH:mm 로 표시용 포맷."""
    if not dtstr:
        return ""
    s = dtstr.replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            continue
    return s  # 파싱 실패 시 원문 그대로


def _as_int(x):
    try:
        return int(x)
    except Exception:
        return 0


# ---------------------------
# 홈
# ---------------------------
def home(request):
    return render(request, "home.html")


# ---------------------------
# 새 폼 화면 (로그인 필요, GET만)
# 폼 제출은 agreement_submit 로 POST
# ---------------------------
@login_required
@require_http_methods(["GET"])
def agreement_form(request, pk=None):
    """
    pk는 현재 미사용(향후 편집 전용으로 확장 가능).
    화면은 accident_project/form.html 하나로 고정.
    """
    return render(
        request,
        "accident_project/form.html",
        {
            "agreement": None,            # 템플릿 호환 슬롯
            "part_anchors": PART_ANCHORS, # 차량 마킹용 좌표 사전
            "label_colors": LABEL_COLORS,
        },
    )


# ---------------------------
# 저장(POST) → 생성 후 print 화면으로 리다이렉트
# ---------------------------
@login_required
@require_http_methods(["POST"])
def agreement_submit(request: HttpRequest):
    P = request.POST
    F = {
        # 메타
        "accident_date": P.get("accident_date") or "",
        "location": P.get("location") or "",
        # A
        "a_plate": P.get("a_plate") or "",
        "a_insurer": P.get("a_insurer") or "",
        "a_name": P.get("a_name") or "",
        "a_id": P.get("a_id") or "",
        "a_phone": P.get("a_phone") or "",
        "a_address": P.get("a_address") or "",
        "a_male": P.get("a_male") or "0",
        "a_female": P.get("a_female") or "0",
        "a_damage_desc": P.get("a_damage_desc") or "",
        # B
        "b_plate": P.get("b_plate") or "",
        "b_insurer": P.get("b_insurer") or "",
        "b_name": P.get("b_name") or "",
        "b_id": P.get("b_id") or "",
        "b_phone": P.get("b_phone") or "",
        "b_address": P.get("b_address") or "",
        "b_male": P.get("b_male") or "0",
        "b_female": P.get("b_female") or "0",
        "b_damage_desc": P.get("b_damage_desc") or "",
        # 보행자(선택)
        "p_name": P.get("p_name") or "",
        "p_id": P.get("p_id") or "",
        "p_phone": P.get("p_phone") or "",
        "p_address": P.get("p_address") or "",
        "p_damage_desc": P.get("p_damage_desc") or "",
        # 배열
        "weather": P.getlist("weather"),
        "type_cc": P.getlist("type_cc"),
        "type_cp": P.getlist("type_cp"),
        "cause": P.getlist("cause"),
        # 서술
        "accident_description": P.get("accident_description") or "",
        # 선택부위(JSON 문자열)
        "a_parts_json": P.get("a_parts_json") or "[]",
        "b_parts_json": P.get("b_parts_json") or "[]",
    }

    rec = Agreement.objects.create(
        owner=request.user,
        incident_dt=F["accident_date"],
        location=F["location"],
        a_name=F["a_name"],
        b_name=F["b_name"],
        damages_raw=json.dumps(F, ensure_ascii=False),
    )

    out_format = P.get("format", "pdf")
    mask_rrn = P.get("mask_rrn") in ("true", "on", "1")

    url = reverse("accident_project:agreement_print", kwargs={"pk": rec.pk})
    url += f"?mask_rrn={'true' if mask_rrn else 'false'}&format={out_format}"
    return redirect(url)


# ---------------------------
# 최종 출력(서버 템플릿 렌더)
# ---------------------------
@login_required
def agreement_print(request: HttpRequest, pk: int):
    rec, F = _get_agreement_payload_or_404(pk)
    if rec.owner_id != request.user.id:
        return HttpResponseForbidden("본인 문서만 조회할 수 있습니다.")

    F = dict(F)  # 가변 복사

    # 배열 복원
    try:
        F["a_parts"] = json.loads(F.get("a_parts_json") or "[]")
    except Exception:
        F["a_parts"] = []
    try:
        F["b_parts"] = json.loads(F.get("b_parts_json") or "[]")
    except Exception:
        F["b_parts"] = []

    # 마스킹 옵션
    mask = request.GET.get("mask_rrn") in ("true", "on", "1")
    if mask:
        F["a_id_masked"] = mask_rrn_value(F.get("a_id"))
        F["b_id_masked"] = mask_rrn_value(F.get("b_id"))
        F["p_id_masked"] = mask_rrn_value(F.get("p_id"))

    # 표시용
    F["accident_date_display"] = _fmt_k(F.get("accident_date"))
    F["a_total"] = str(_as_int(F.get("a_male")) + _as_int(F.get("a_female")))
    F["b_total"] = str(_as_int(F.get("b_male")) + _as_int(F.get("b_female")))

    return render(
        request,
        "accident_project/print.html",
        {
            "F": F,
            "pk": rec.pk,
            "mask_rrn": mask,
            "part_anchors": PART_ANCHORS,
            "label_colors": LABEL_COLORS,
        },
    )


# ---------------------------
# 서버 PDF/JPG 다운로드 (단순 Fallback)
# ---------------------------
@login_required
def agreement_pdf(request, pk):
    rec, data = _get_agreement_payload_or_404(pk)
    if rec.owner_id != request.user.id:
        return HttpResponseForbidden("본인 문서만 다운로드할 수 있습니다.")

    buf = BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    y = h - 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(180, y, "Traffic Accident Agreement")
    y -= 30
    p.setFont("Helvetica", 11)
    lines = [
        ("사고일시", data.get("accident_date", "")),
        ("사고장소", data.get("location", "")),
        ("A차량 운전자", data.get("a_name", "")),
        ("B차량 운전자", data.get("b_name", "")),
        ("A차량 번호", data.get("a_plate", "")),
        ("B차량 번호", data.get("b_plate", "")),
        ("사고 개요", data.get("accident_description", "")),
    ]
    for k, v in lines:
        p.drawString(60, y, f"{k}: {v}")
        y -= 18
        if y < 40:
            p.showPage()
            y = h - 40
            p.setFont("Helvetica", 11)
    p.save()
    buf.seek(0)

    filename = f"agreement_{pk}.pdf"
    resp = HttpResponse(buf.getvalue(), content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


@login_required
def agreement_image(request, pk):
    rec, data = _get_agreement_payload_or_404(pk)
    if rec.owner_id != request.user.id:
        return HttpResponseForbidden("본인 문서만 다운로드할 수 있습니다.")

    content = f"""교통사고 협의서(요약)
사고일시: {data.get('accident_date','')}
사고장소: {data.get('location','')}
A 운전자: {data.get('a_name','')}  / 차량: {data.get('a_plate','')}
B 운전자: {data.get('b_name','')}  / 차량: {data.get('b_plate','')}
사고 개요: {data.get('accident_description','')}
"""
    filename = f"agreement_{pk}.txt"
    resp = HttpResponse(content, content_type="text/plain; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


# ---------------------------
# 미리보기(로컬스토리지 기반) → print.html 재사용
# ---------------------------
@require_http_methods(["GET"])
def agreement_preview(request: HttpRequest):
    F = {
        "accident_date": "",
        "location": "",
        "weather": [],
        "a_plate": "",
        "a_insurer": "",
        "a_name": "",
        "a_id": "",
        "a_phone": "",
        "a_address": "",
        "a_male": "0",
        "a_female": "0",
        "a_damage_desc": "",
        "a_parts": [],
        "a_markers": [],
        "b_plate": "",
        "b_insurer": "",
        "b_name": "",
        "b_id": "",
        "b_phone": "",
        "b_address": "",
        "b_male": "0",
        "b_female": "0",
        "b_damage_desc": "",
        "b_parts": [],
        "b_markers": [],
        "p_name": "",
        "p_id": "",
        "p_phone": "",
        "p_address": "",
        "p_damage_desc": "",
        "type_cc": [],
        "type_cp": [],
        "cause": [],
        "accident_description": "",
    }
    return render(
        request,
        "accident_project/print.html",
        {
            "F": F,
            "pk": None,
            "mask_rrn": False,
            "part_anchors": PART_ANCHORS,
            "label_colors": LABEL_COLORS,
        },
    )


# ---------------------------
# 마이페이지(레거시 AccidentRecord 유지)
# ---------------------------
@login_required
def mypage(request):
    qs = AccidentRecord.objects.filter(owner=request.user).order_by(
        "-accident_date", "-id"
    )
    page = Paginator(qs, 3).get_page(request.GET.get("page"))
    ctx = {
        "agreements": page,  # 템플릿 호환용 이름 유지
        "user": request.user,
    }
    return render(request, "accident_project/mypage.html", ctx)


# ---------------------------
# Agreement 목록(정식)
# ---------------------------
@login_required
def mypage_agreements(request):
    qs = Agreement.objects.filter(owner=request.user).order_by("-created_at")
    return render(
        request, "accident_project/mypage_agreements.html", {"agreements": qs}
    )

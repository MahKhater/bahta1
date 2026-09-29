import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات

questions_db = [
    # -----------------------------------------------------------------
    # أولاً: المستوى المبتدئ (50 سؤالاً مباشراً وأساسياً)
    # -----------------------------------------------------------------
    {"id": 1, "level": "مبتدئ", "question": "ما هو مجال الدالة الثابتة: f(x) = 5 ؟", "options": ["ح", "{5}", "[0, مالا نهائية)", "ح - {0}"], "answer": "ح"},
    {"id": 2, "level": "مبتدئ", "question": "ما هو مدى الدالة الثابتة: f(x) = -3 ؟", "options": ["{-3}", "ح", "[0, مالا نهائية)", "ح - {-3}"], "answer": "{-3}"},
    {"id": 3, "level": "مبتدئ", "question": "ما هو مجال الدالة الخطية: f(x) = 2x + 1 ؟", "options": ["ح", "ح - {0}", "[0, مالا نهائية)", "ح*"], "answer": "ح"},
    {"id": 4, "level": "مبتدئ", "question": "ما هو مجال الدالة الكسرية: f(x) = 1 / (x - 2) ؟", "options": ["ح", "ح - {2}", "ح - {-2}", "[2, مالا نهائية)"], "answer": "ح - {2}"},
    {"id": 5, "level": "مبتدئ", "question": "ما هو مجال الدالة الكسرية: f(x) = 5 / (x + 4) ؟", "options": ["ح - {-4}", "ح - {4}", "ح", "[-4, مالا نهائية)"], "answer": "ح - {-4}"},
    {"id": 6, "level": "مبتدئ", "question": "ما هو مجال دالة الكثيرات الحدود: f(x) = x^3 - 3x + 2 ؟", "options": ["ح", "ح - {0}", "[0, مالا نهائية)", "ح*"], "answer": "ح"},
    {"id": 7, "level": "مبتدئ", "question": "ما هو مدى الدالة التربيعية: f(x) = x^2 ؟", "options": ["[0, مالا نهائية)", "ح", "(-مالا نهائية, 0]", "ح - {0}"], "answer": "[0, مالا نهائية)"},
    {"id": 8, "level": "مبتدئ", "question": "ما هو مجال الدالة الجذرية: f(x) = جذر(x) ؟", "options": ["[0, مالا نهائية)", "ح", "(0, مالا نهائية)", "ح - {0}"], "answer": "[0, مالا نهائية)"},
    {"id": 9, "level": "مبتدئ", "question": "ما هو مجال الدالة الجذرية: f(x) = جذر(x - 3) ؟", "options": ["[3, مالا نهائية)", "ح - {3}", "(3, مالا نهائية)", "ح"], "answer": "[3, مالا نهائية)"},
    {"id": 10, "level": "مبتدئ", "question": "ما هو مجال الدالة الجذرية: f(x) = جذر(5 - x) ؟", "options": ["(-مالا نهائية, 5]", "[5, مالا نهائية)", "ح - {5}", "ح"], "answer": "(-مالا نهائية, 5]"},
    {"id": 11, "level": "مبتدئ", "question": "نقطة رأس المنظومة للدالة f(x) = (x - 2)^2 + 3 هي:", "options": ["(2, 3)", "(-2, 3)", "(2, -3)", "(-2, -3)"], "answer": "(2, 3)"},
    {"id": 12, "level": "مبتدئ", "question": "نقطة تماثل منحنى دالة المقلوب f(x) = 1/x هي:", "options": ["(0, 0)", "(1, 1)", "(0, 1)", "(1, 0)"], "answer": "(0, 0)"},
    {"id": 13, "level": "مبتدئ", "question": "الدالة f(x) = x^3 تعتبر دالة:", "options": ["فردية", "زوجية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "فردية"},
    {"id": 14, "level": "مبتدئ", "question": "الدالة f(x) = x^2 تعتبر دالة:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "أحادية"], "answer": "زوجية"},
    {"id": 15, "level": "مبتدئ", "question": "الدالة f(x) = |x| تعتبر دالة:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "صفرية"], "answer": "زوجية"},
    {"id": 16, "level": "مبتدئ", "question": "إشارة الدالة f(x) = 7 تكون موجبة في:", "options": ["ح", "ح - {0}", "[0, مالا نهائية)", "فارغة"], "answer": "ح"},
    {"id": 17, "level": "مبتدئ", "question": "مدى الدالة f(x) = |x| هو:", "options": ["[0, مالا نهائية)", "ح", "(-مالا نهائية, 0]", "ح - {0}"], "answer": "[0, مالا نهائية)"},
    {"id": 18, "level": "مبتدئ", "question": "مدى الدالة الجذرية f(x) = جذر(x) هو:", "options": ["[0, مالا نهائية)", "ح", "(0, مالا نهائية)", "ح - {0}"], "answer": "[0, مالا نهائية)"},
    {"id": 19, "level": "مبتدئ", "question": "مجال الدالة f(x) = 3 / (x^2 - 1) هو:", "options": ["ح - {1, -1}", "ح - {1}", "ح - {-1}", "ح"], "answer": "ح - {1, -1}"},
    {"id": 20, "level": "مبتدئ", "question": "إذا كانت f(x) = 2x - 4، فإن f(3) تساوي:", "options": ["2", "6", "0", "-2"], "answer": "2"},
    {"id": 21, "level": "مبتدئ", "question": "إذا كانت f(x) = x^2 - 1، فإن f(-2) تساوي:", "options": ["3", "5", "-5", "4"], "answer": "3"},
    {"id": 22, "level": "مبتدئ", "question": "ما هو مجال الدالة f(x) = 1 / (x^2 + 4) ؟", "options": ["ح", "ح - {2, -2}", "ح - {4}", "[4, مالا نهائية)"], "answer": "ح"},
    {"id": 23, "level": "مبتدئ", "question": "منحنى الدالة f(x) = (x - 1)^2 يبتعد عن نقطة الأصل بمقدار وحدة واحدة إلى:", "options": ["اليمين", "اليسار", "الأعلى", "أسفل"], "answer": "اليمين"},
    {"id": 24, "level": "مبتدئ", "question": "منحنى الدالة f(x) = x^2 + 4 يرتفع عن نقطة الأصل بمقدار:", "options": ["4 وحدات للأعلى", "4 وحدات لليسار", "4 وحدات لليمين", "4 وحدات لأسفل"], "answer": "4 وحدات للأعلى"},
    {"id": 25, "level": "مبتدئ", "question": "الدالة f(x) = x^5 تكون:", "options": ["فردية", "زوجية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "فردية"},
    {"id": 26, "level": "مبتدئ", "question": "الدالة f(x) = x^4 - x^2 تكون:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "صفرية"], "answer": "زوجية"},
    {"id": 27, "level": "مبتدئ", "question": "إذا كانت f دالة فردية، فإن f(-x) يساوي:", "options": ["-f(x)", "f(x)", "0", "1"], "answer": "-f(x)"},
    {"id": 28, "level": "مبتدئ", "question": "مجال الدالة f(x) = جذر التكعيبي لـ (x) هو:", "options": ["ح", "[0, مالا نهائية)", "ح - {0}", "(0, مالا نهائية)"], "answer": "ح"},
    {"id": 29, "level": "مبتدئ", "question": "مدى الدالة f(x) = جذر التكعيبي لـ (x) هو:", "options": ["ح", "[0, مالا نهائية)", "ح - {0}", "(0, مالا نهائية)"], "answer": "ح"},
    {"id": 30, "level": "مبتدئ", "question": "القيمة العظمى أو الصغرى للدالة f(x) = (x - 3)^2 + 5 هي:", "options": ["صغرى عند 5", "عظمى عند 5", "صغرى عند 3", "عظمى عند 3"], "answer": "صغرى عند 5"},
    {"id": 31, "level": "مبتدئ", "question": "ما هو مجال الدالة: f(x) = 4 / (2x - 6) ؟", "options": ["ح - {3}", "ح - {-3}", "ح", "[3, مالا نهائية)"], "answer": "ح - {3}"},
    {"id": 32, "level": "مبتدئ", "question": "ما هو مجال الدالة: f(x) = 1 / (3x + 9) ؟", "options": ["ح - {-3}", "ح - {3}", "ح", "[-3, مالا نهائية)"], "answer": "ح - {-3}"},
    {"id": 33, "level": "مبتدئ", "question": "الدالة f(x) = |x - 2| متماثلة حول المستقيم:", "options": ["x = 2", "x = -2", "y = 2", "y = 0"], "answer": "x = 2"},
    {"id": 34, "level": "مبتدئ", "question": "إشارة الدالة f(x) = -5 تكون سالبة في:", "options": ["ح", "ح - {0}", "[0, مالا نهائية)", "فارغة"], "answer": "ح"},
    {"id": 35, "level": "مبتدئ", "question": "مدى الدالة الثابتة f(x) = -7 هو:", "options": ["{-7}", "ح", "[0, مالا نهائية)", "ح - {-7}"], "answer": "{-7}"},
    {"id": 36, "level": "مبتدئ", "question": "نوع الدالة f(x) = x^3 + x هو:", "options": ["فردية", "زوجية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "فردية"},
    {"id": 37, "level": "مبتدئ", "question": "نوع الدالة f(x) = x^2 + x هو:", "options": ["ليست زوجية وليست فردية", "زوجية", "فردية", "ثابتة"], "answer": "ليست زوجية وليست فردية"},
    {"id": 38, "level": "مبتدئ", "question": "مجال الدالة f(x) = جذر(x + 5) هو:", "options": ["[-5, مالا نهائية)", "ح - {-5}", "( -5, مالا نهائية)", "ح"], "answer": "[-5, مالا نهائية)"},
    {"id": 39, "level": "مبتدئ", "question": "مجال الدالة f(x) = جذر(7 - x) هو:", "options": ["(-مالا نهائية, 7]", "[7, مالا نهائية)", "ح - {7}", "ح"], "answer": "(-مالا نهائية, 7]"},
    {"id": 40, "level": "مبتدئ", "question": "إذا كانت f(x) = 3x^2، فإن f(-1) تساوي:", "options": ["3", "-3", "9", "-9"], "answer": "3"},
    {"id": 41, "level": "مبتدئ", "question": "منحنى الدالة f(x) = -(x^2) يتميز بأنه:", "options": ["مفتوح لأَسفل وله قيمة عظمى", "مفتوح لأعلى وله قيمة صغرى", "خط مستقيم", "دالة كسرية"], "answer": "مفتوح لأَسفل وله قيمة عظمى"},
    {"id": 42, "level": "مبتدئ", "question": "نقطة تماثل دالة الجذر التكعيبي f(x) = جذر تكعيبي(x - 1) + 2 هي:", "options": ["(1, 2)", "(-1, 2)", "(1, -2)", "(-1, -2)"], "answer": "(1, 2)"},
   {"id": 43, "level": "مبتدئ", "question": "الدالة f(x) = -5x تكون تناقصية لأن معامل x:", "options": ["سالب", "موجب", "صفر", "لا يوجد إجابة"], "answer": "سالب"},
    {"id": 44, "level": "مبتدئ", "question": "مجال الدالة f(x) = 2 / (x^2 - 16) هو:", "options": ["ح - {4, -4}", "ح - {16}", "ح", "[0, 16]"], "answer": "ح - {4, -4}"},
    {"id": 45, "level": "مبتدئ", "question": "أي من الدوال الآتية تمثل دالة زوجية؟", "options": ["f(x) = x^2 + 1", "f(x) = x^3", "f(x) = x + 1", "f(x) = x^3 - x"], "answer": "f(x) = x^2 + 1"},
    {"id": 46, "level": "مبتدئ", "question": "أي من الدوال الآتية تمثل دالة فردية؟", "options": ["f(x) = x^3 - x", "f(x) = x^2", "f(x) = |x|", "f(x) = 5"], "answer": "f(x) = x^3 - x"},
    {"id": 47, "level": "مبتدئ", "question": "مدى الدالة f(x) = -|x| هو:", "options": ["(-مالا نهائية, 0]", "[0, مالا نهائية)", "ح", "ح - {0}"], "answer": "(-مالا نهائية, 0]"},
    {"id": 48, "level": "مبتدئ", "question": "المستقيمان اللذان يمثلان خطي التقارب لدالة المقلوب f(x) = 1/x هما:", "options": ["محور السينات ومحور الصادات", "المستقيمان x=1 و y=1", "المستقيمان x=2 و y=0", "لا توجد خطوط تقارب"], "answer": "محور السينات ومحور الصادات"},
    {"id": 49, "level": "مبتدئ", "question": "إذا كانت نقطة رأس المنحنى (2, -3)، فإن معادلة محور التماثل هي:", "options": ["x = 2", "x = -3", "y = 2", "y = -3"], "answer": "x = 2"},
    {"id": 50, "level": "مبتدئ", "question": "ما هو مجال الدالة f(x) = 1 / (x(x - 3)) هو:", "options": ["ح - {0, 3}", "ح - {3}", "ح - {0}", "ح"], "answer": "ح - {0, 3}"},

    # -----------------------------------------------------------------
    # ثانياً: المستوى المتوسط (50 سؤالاً تتطلب خطوات أعمق)
    # -----------------------------------------------------------------
    {"id": 51, "level": "متوسط", "question": "ما هو مجال الدالة: f(x) = 1 / (x^2 - 9) ؟", "options": ["ح - {3, -3}", "ح - {9}", "ح", "[-3, 3]"], "answer": "ح - {3, -3}"},
    {"id": 52, "level": "متوسط", "question": "ما هو مدى الدالة التربيعية: f(x) = x^2 + 3 ؟", "options": ["[3, مالا نهائية)", "ح", "(-مالا نهائية, 3]", "ح - {3}"], "answer": "[3, مالا نهائية)"},
    {"id": 53, "level": "متوسط", "question": "ما هو مجال الدالة: f(x) = جذر(x - 2) + جذر(5 - x) ؟", "options": ["[2, 5]", "ح - {2, 5}", "(2, 5)", "ح"], "answer": "[2, 5]"},
    {"id": 54, "level": "متوسط", "question": "ما هو مجال الدالة: f(x) = 1 / جذر(x - 4) ؟", "options": ["(4, مالا نهائية)", "[4, مالا نهائية)", "ح - {4}", "[0, 4]"], "answer": "(4, مالا نهائية)"},
    {"id": 55, "level": "متوسط", "question": "مدى الدالة f(x) = 5 - |x| هو:", "options": ["(-مالا نهائية, 5]", "[5, مالا نهائية)", "ح", "[0, 5]"], "answer": "(-مالا نهائية, 5]"},
    {"id": 56, "level": "متوسط", "question": "إذا كانت f(x) = x^2 - 4x + 5، فإن القيمة الصغرى للدالة هي:", "options": ["1", "5", "-4", "0"], "answer": "1"},
    {"id": 57, "level": "متوسط", "question": "مجال الدالة f(x) = جذر(x^2 - 9) هو:", "options": ["(-مالا نهائية, -3] اتحاد [3, مالا نهائية)", "[-3, 3]", "ح - {-3, 3}", "ح"], "answer": "(-مالا نهائية, -3] اتحاد [3, مالا نهائية)"},
    {"id": 58, "level": "متوسط", "question": "بحث اضطراد الدالة f(x) = -(x - 1)^2 يكون تناقصياً في الفترة:", "options": ["[1, مالا نهائية)", "(-مالا نهائية, 1]", "ح", "[-1, مالا نهائية)"], "answer": "[1, مالا نهائية)"},
    {"id": 59, "level": "متوسط", "question": "بحث اضطراد الدالة f(x) = (x - 2)^2 يكون تزايدياً في الفترة:", "options": ["[2, مالا نهائية)", "(-مالا نهائية, 2]", "ح", "[0, 2]"], "answer": "[2, مالا نهائية)"},
    {"id": 60, "level": "متوسط", "question": "ما هو مدى الدالة f(x) = 2 / x هو:", "options": ["ح - {0}", "ح", "[0, مالا نهائية)", "(0, مالا نهائية)"], "answer": "ح - {0}"},
    {"id": 61, "level": "متوسط", "question": "نوع الدالة f(x) = (x^3) / (x^2 + 1) هو:", "options": ["فردية", "زوجية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "فردية"},
    {"id": 62, "level": "متوسط", "question": "نوع الدالة f(x) = (x^2) / (|x| + 1) هو:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "أحادية"], "answer": "زوجية"},
    {"id": 63, "level": "متوسط", "question": "مجال الدالة المعرفة بقاعدتين: f(x) = x للـ x >= 0 و -x للـ x < 0 هو:", "options": ["ح", "[0, مالا نهائية)", "ح - {0}", "فارغة"], "answer": "ح"},
    {"id": 64, "level": "متوسط", "question": "مدى الدالة f(x) = |x| / x عندما x لا تساوي الصفر هو:", "options": ["{-1, 1}", "ح", "[0, 1]", "{0, 1}"], "answer": "{-1, 1}"},
    {"id": 65, "level": "متوسط", "question": "إذا كانت f(x) = 3^x، فإن مدى الدالة هو:", "options": ["(0, مالا نهائية)", "ح", "[0, مالا نهائية)", "ح - {0}"], "answer": "(0, مالا نهائية)"},
    {"id": 66, "level": "متوسط", "question": "ما هو مجال الدالة f(x) = جذر(x + 1) / (x - 3) هو:", "options": ["[-1, مالا نهائية) ما عدا {3}", "ح - {3}", "[-1, 3] اتحاد (3, مالا نهائية)", "ح"], "answer": "[-1, مالا نهائية) ما عدا {3}"},
    {"id": 67, "level": "متوسط", "question": "إشارة الدالة f(x) = x^2 - 4 تكون سالبة في الفترة:", "options": ["(-2, 2)", "ح - [-2, 2]", "(-مالا نهائية, -2)", "(2, مالا نهائية)"], "answer": "(-2, 2)"},
    {"id": 68, "level": "متوسط", "question": "إشارة الدالة f(x) = 9 - x^2 تكون موجبة في الفترة:", "options": ["(-3, 3)", "ح - [-3, 3]", "(-مالا نهائية, -3]", "[3, مالا نهائية)"], "answer": "(-3, 3)"},
    {"id": 69, "level": "متوسط", "question": "إذا كانت f(x) = x - 2 و g(x) = x^2، فإن (فه)(3) أو (f o g)(3) تساوي:", "options": ["7", "1", "9", "5"], "answer": "7"},
    {"id": 70, "level": "متوسط", "question": "إذا كانت f(x) = 2x و g(x) = x + 3، فإن (g o f)(2) تساوي:", "options": ["7", "10", "4", "5"], "answer": "7"},
    {"id": 71, "level": "متوسط", "question": "مجال الدالة f(x) = جذر(2x - 6) هو:", "options": ["[3, مالا نهائية)", "(3, مالا نهائية)", "ح - {3}", "[-3, مالا نهائية)"], "answer": "[3, مالا نهائية)"},
    {"id": 72, "level": "متوسط", "question": "مدى الدالة f(x) = -|x - 2| + 4 هو:", "options": ["(-مالا نهائية, 4]", "[4, مالا نهائية)", "ح", "[0, 4]"], "answer": "(-مالا نهائية, 4]"},
    {"id": 73, "level": "متوسط", "question": "نقطة رأس المنحنى للدالة f(x) = -2(x + 1)^2 - 5 هي:", "options": ["(-1, -5)", "(1, -5)", "(-1, 5)", "(1, 5)"], "answer": "(-1, -5)"},
    {"id": 74, "level": "متوسط", "question": "الدالة العكسية للدالة الخطية f(x) = 2x + 4 هي:", "options": ["f^-1(x) = (x - 4) / 2", "f^-1(x) = 2x - 4", "f^-1(x) = x / 2 - 4", "فارغة"], "answer": "f^-1(x) = (x - 4) / 2"},
    {"id": 75, "level": "متوسط", "question": "الدالة العكسية للدالة f(x) = x - 3 هي:", "options": ["f^-1(x) = x + 3", "f^-1(x) = 3 - x", "f^-1(x) = x / 3", "f^-1(x) = 3x"], "answer": "f^-1(x) = x + 3"},
    {"id": 76, "level": "متوسط", "question": "إذا كانت الدالة أحادية وكانت f(2) = 5، فإن f^-1(5) تساوي:", "options": ["2", "-2", "1/5", "5"], "answer": "2"},
    {"id": 77, "level": "متوسط", "question": "ما هو مجال الدالة f(x) = 1 / (جذر(x) - 2) هو:", "options": ["[0, 4) اتحاد (4, مالا نهائية)", "[0, مالا نهائية)", "ح - {4}", "(4, مالا نهائية)"], "answer": "[0, 4) اتحاد (4, مالا نهائية)"},
    {"id": 78, "level": "متوسط", "question": "منحنى الدالة f(x) = (x + 3)^2 - 2 ينتج من منحنى y = x^2 بإزاحة مقدارها:", "options": ["3 وحدات لليسار و 2 وحدة لأسفل", "3 وحدات لليمين و 2 لأعلى", "3 وحدات لليمين و 2 لأسفل", "3 لليسار و 2 لأعلى"], "answer": "3 وحدات لليسار و 2 وحدة لأسفل"},
    {"id": 79, "level": "متوسط", "question": "إذا كانت f(x) دالة زوجية متصلة على ح وكان انتماؤها محدد، فإن f(0) إن لم تحدد تقبل قيم:", "options": ["أي قيمة حقيقية بشرط تحقق التماثل", "صفر حصراً", "1 حصراً", "غير معرفة"], "answer": "أي قيمة حقيقية بشرط تحقق التماثل"},
    {"id": 80, "level": "متوسط", "question": "مجال الدالة f(x) = جذر(4 - x^2) هو:", "options": ["[-2, 2]", "(-مالا نهائية, -2] اتحاد [2, مالا نهائية)", "ح - {-2, 2}", "ح"], "answer": "[-2, 2]"},
    {"id": 81, "level": "متوسط", "question": "مدى الدالة f(x) = جذر(4 - x^2) هو:", "options": ["[0, 2]", "[-2, 2]", "[0, 4]", "ح"], "answer": "[0, 2]"},
    {"id": 82, "level": "متوسط", "question": "إشارة الدالة f(x) = 2x - 6 تكون موجبة عندما:", "options": ["x > 3", "x < 3", "x = 3", "ح"], "answer": "x > 3"},
    {"id": 83, "level": "متوسط", "question": "إشارة الدالة f(x) = 8 - 2x تكون سالبة عندما:", "options": ["x > 4", "x < 4", "x = 4", "ح"], "answer": "x > 4"},
    {"id": 84, "level": "متوسط", "question": "الدالة f(x) = x^3 - 2 تكون اضطرادها في مجالها:", "options": ["تزايدية على ح", "تناقصية على ح", "ثابتة", "تزايدية في فترة وتناقصية في أخرى"], "answer": "تزايدية على ح"},
    {"id": 85, "level": "متوسط", "question": "الدالة f(x) = -x^3 تكون اضطرادها في مجالها:", "options": ["تناقصية على ح", "تزايدية على ح", "ثابتة", "تزايدية وتناقصية"], "answer": "تناقصية على ح"},
    {"id": 86, "level": "متوسط", "question": "إذا كانت نقطة رأس التماثل لدالة مقلوب محسوبة هي (2، 3)، فإن خطي التقارب هما:", "options": ["x = 2 , y = 3", "x = 3 , y = 2", "x = 0 , y = 0", "x = -2 , y = -3"], "answer": "x = 2 , y = 3"},
    {"id": 87, "level": "متوسط", "question": "مجال الدالة f(x) = 1 / (|x| - 3) هو:", "options": ["ح - {3, -3}", "ح - {3}", "[-3, 3]", "ح"], "answer": "ح - {3, -3}"},
    {"id": 88, "level": "متوسط", "question": "مدى الدالة f(x) = 3 + جذر(x - 1) هو:", "options": ["[3, مالا نهائية)", "ح", "[1, مالا نهائية)", "(3, مالا نهائية)"], "answer": "[3, مالا نهائية)"},
    {"id": 89, "level": "متوسط", "question": "إذا كانت f(x) = x^2 للـ x >= 0 و x للـ x < 0، فان f(-3) تساوي:", "options": ["-3", "9", "3", "0"], "answer": "-3"},
    {"id": 90, "level": "متوسط", "question": "إذا كانت f(x) = x^2 للـ x >= 0 و x للـ x < 0، فان f(3) تساوي:", "options": ["9", "3", "-3", "0"], "answer": "9"},
    {"id": 91, "level": "متوسط", "question": "نوع الدالة f(x) = x^6 + x^4 + 1 هو:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "أحادية"], "answer": "زوجية"},
    {"id": 92, "level": "متوسط", "question": "نوع الدالة f(x) = sin(x) (في دراسة الدوال المثلثية إن وجدت) أو f(x) = x|x| هو:", "options": ["فردية", "زوجية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "فردية"},
    {"id": 93, "level": "متوسط", "question": "إذا كان منحنى الدالة متماثلاً حول محور الصادات، فإن الدالة تكون:", "options": ["زوجية", "فردية", "أحادية", "تزايدية"], "answer": "زوجية"},
    {"id": 94, "level": "متوسط", "question": "إذا كان منحنى الدالة متماثلاً حول نقطة الأصل، فإن الدالة تكون:", "options": ["فردية", "زوجية", "ثابتة", "تناقصية"], "answer": "فردية"},
    {"id": 95, "level": "متوسط", "question": "مجال الدالة f(x) = جذر التكعيبي لـ (x - 2) / (x - 5) هو:", "options": ["ح - {5}", "ح", "[2, مالا نهائية)", "ح - {2, 5}"], "answer": "ح - {5}"},
    {"id": 96, "level": "متوسط", "question": "مدى الدالة f(x) = -|x| - 2 هو:", "options": ["(-مالا نهائية, -2]", "[-2, مالا نهائية)", "ح", "ح - {-2}"], "answer": "(-مالا نهائية, -2]"},
    {"id": 97, "level": "متوسط", "question": "القيمة العظمى للدالة f(x) = 4 - (x - 1)^2 هي:", "options": ["4 عند x = 1", "-4 عند x = 1", "1 عند x = 4", "صفر"], "answer": "4 عند x = 1"},
    {"id": 98, "level": "متوسط", "question": "إذا كانت f(x) = 5^x - 1، فإن تقاطع المنحنى مع محور الصادات يحدث عند نقطة:", "options": ["(0, 0)", "(0, 1)", "(1, 0)", "(0, 4)"], "answer": "(0, 0)"},
    {"id": 99, "level": "متوسط", "question": "مجال الدالة f(x) = 1 / (x^2 - 5x + 6) هو:", "options": ["ح - {2, 3}", "ح - {-2, -3}", "ح - {6}", "ح"], "answer": "ح - {2, 3}"},
    {"id": 100, "level": "متوسط", "question": "إذا كانت f(x) دالة زوجية ومعرفة على [-3, 3] وكان لها قاعدة، فإن مجموع f(2) + f(-2) إذا كانت f(2)=4 يساوي:", "options": ["8", "4", "0", "-8"], "answer": "8"},

    # -----------------------------------------------------------------
    # ثالثاً: المستوى المتقدم (50 سؤالاً تفكير عليا وتركيب مهارات)
    # -----------------------------------------------------------------
    {"id": 101, "level": "متقدم", "question": "ما هو مجال الدالة: f(x) = 1 / جذر(x^2 - 5x + 6) ؟", "options": ["(-مالا نهائية, 2) اتحاد (3, مالا نهائية)", "(2, 3)", "ح - {2, 3}", "[2, 3]"], "answer": "(-مالا نهائية, 2) اتحاد (3, مالا نهائية)"},
    {"id": 102, "level": "متقدم", "question": "إذا كانت f دالة زوجية ومجالها [-a, a]، فإن حاصل ضرب f(x) * g(x) حيث g فردية يكون:", "options": ["دالة فردية", "دالة زوجية", "ليست زوجية وليست فردية", "صفرية دائماً"], "answer": "دالة فردية"},
    {"id": 103, "level": "متقدم", "question": "ما هو مدى الدالة: f(x) = |x - 2| / (x - 2) عندما x لا تساوي 2:", "options": ["{-1, 1}", "ح", "[0, 1]", "{-1, 0, 1}"], "answer": "{-1, 1}"},
    {"id": 104, "level": "متقدم", "question": "مجال الدالة f(x) = جذر(x) + جذر(1 - x) هو:", "options": ["[0, 1]", "(-مالا نهائية, 1]", "[0, مالا نهائية)", "ح"], "answer": "[0, 1]"},
    {"id": 105, "level": "متقدم", "question": "إذا كانت f(x) = x^2 + 1 و g(x) = جذر(x - 1)، فإن مجال التركيب (f o g)(x) هو:", "options": ["[1, مالا نهائية)", "ح", "(1, مالا نهائية)", "[0, مالا نهائية)"], "answer": "[1, مالا نهائية)"},
    {"id": 106, "level": "متقدم", "question": "إذا كانت f(x) = x / (x - 1)، فإن الدالة العكسية f^-1(x) تساوي:", "options": ["x / (x - 1)", "(x - 1) / x", "1 / (x - 1)", "x + 1"], "answer": "x / (x - 1)"},
    {"id": 107, "level": "متقدم", "question": "ما هو مدى الدالة f(x) = (x^2 - 4) / (x - 2) عندما x لا تساوي 2:", "options": ["ح - {4}", "ح", "[0, مالا نهائية)", "ح - {2}"], "answer": "ح - {4}"},
    {"id": 108, "level": "متقدم", "question": "مجال الدالة f(x) = جذر(x^2 - 4x + 4) هو:", "options": ["ح", "[2, مالا نهائية)", "(-مالا نهائية, 2]", "ح - {2}"], "answer": "ح"},
    {"id": 109, "level": "متقدم", "question": "إذا كانت f دالة فردية ومجالها متماثل حول الأصل، وكانت f(0) معرفة، فإن f(0) تساوي حتماً:", "options": ["0", "1", "-1", "لا يمكن تحديدها"], "answer": "0"},
    {"id": 110, "level": "متقدم", "question": "ما هو مجال الدالة f(x) = log(x - 2) (باستخدام خصائص الدوال الحقيقية المرتبطة) أو جذر المراتب: جذر رابع لـ (5 - x) هو:", "options": ["(-مالا نهائية, 5]", "[5, مالا نهائية)", "(5, مالا نهائية)", "ح"], "answer": "(-مالا نهائية, 5]"},
    {"id": 111, "level": "متقدم", "question": "إذا كانت f(x) = |x + 1| + |x - 1|، فإن مدى الدالة هو:", "options": ["[2, مالا نهائية)", "[0, مالا نهائية)", "ح", "[1, مالا نهائية)"], "answer": "[2, مالا نهائية)"},
    {"id": 112, "level": "متقدم", "question": "القيمة الصغرى للدالة f(x) = |x| + |x - 3| هي:", "options": ["3", "0", "-3", "1.5"], "answer": "3"},
    {"id": 113, "level": "متقدم", "question": "مجال الدالة f(x) = 1 / (جذر(4 - x^2)) هو:", "options": ["(-2, 2)", "[-2, 2]", "ح - {-2, 2}", "[-2, 2) اتحاد (2, مالا نهائية)"], "answer": "(-2, 2)"},
    {"id": 114, "level": "متقدم", "question": "إذا كانت f(x) دالة زوجية و g دالة زوجية، فإن الدالة h(x) = f(x) + g(x) تكون:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "صفرية"], "answer": "زوجية"},
    {"id": 115, "level": "متقدم", "question": "إذا كانت f(x) دالة فردية و g دالة فردية، فإن الدالة h(x) = f(x) * g(x) تكون:", "options": ["زوجية", "فردية", "ليست زوجية وليست فردية", "ثابتة"], "answer": "زوجية"},
    {"id": 116, "level": "متقدم", "question": "ما هو مدى الدالة f(x) = x^2 / (x^2 + 1) هو:", "options": ["[0, 1)", "[0, 1]", "(0, 1)", "ح - {1}"], "answer": "[0, 1)"},
    {"id": 117, "level": "متقدم", "question": "إذا كانت f(x) = (2x + 1) / (x - 3)، فإن مدى الدالة هو:", "options": ["ح - {2}", "ح - {3}", "ح", "[0, مالا نهائية)"], "answer": "ح - {2}"},
    {"id": 118, "level": "متقدم", "question": "مجال الدالة f(x) = جذر(x - 1) / جذر(3 - x) هو:", "options": ["[1, 3)", "[1, 3]", "(1, 3)", "ح - {3}"], "answer": "[1, 3)"},
    {"id": 119, "level": "متقدم", "question": "إذا كان منحنى الدالة y = f(x) قد أزح بمقدار وحدتين يمين وثلاث وحدات لأعلى لتصبح y = (x - 2)^2 + 3، فإن نقطة رأس المنحنى الأصلي y = x^2 قبل الإزاحة كانت:", "options": ["(0, 0)", "(2, 3)", "(-2, -3)", "(3, 2)"], "answer": "(0, 0)"},
    {"id": 120, "level": "متقدم", "question": "ما هو مجال الدالة f(x) = جذر( |x| - 3 ) هو:", "options": ["(-مالا نهائية, -3] اتحاد [3, مالا نهائية)", "[-3, 3]", "[3, مالا نهائية)", "ح"], "answer": "(-مالا نهائية, -3] اتحاد [3, مالا نهائية)"},
    {"id": 121, "level": "متقدم", "question": "إذا كانت f(x) = x^3 + 2x، فإن الدالة العكسية عند f(1) [باعتبارها أحادية ومجالها ممتد] هي أن f^-1(3) تساوي:", "options": ["1", "3", "0", "-1"], "answer": "1"},
    {"id": 122, "level": "متقدم", "question": "مدى الدالة f(x) = 1 / (x^2 + 1) هو:", "options": ["(0, 1]", "[0, 1]", "ح - {0}", "(0, مالا نهائية)"], "answer": "(0, 1]"},
    {"id": 123, "level": "متقدم", "question": "مجال الدالة f(x) = جذر( 1 - جذر(x) ) هو:", "options": ["[0, 1]", "[1, مالا نهائية)", "ح", "(-مالا نهائية, 1]"], "answer": "[0, 1]"},
    {"id": 124, "level": "متقدم", "question": "إذا كانت f(x) = ax + b دالة خطية وكانت f(2) = 5 و f(4) = 9، فإن قيمة a و b على الترتيب هي:", "options": ["2 و 1", "1 و 2", "3 و -1", "2 و 3"], "answer": "2 و 1"},
    {"id": 125, "level": "متقدم", "question": "عدد نقاط تقاطع منحنى الدالة f(x) = |x - 1| مع محور السينات هو:", "options": ["1", "2", "0", "لا نهائي"], "answer": "1"},
    {"id": 126, "level": "متقدم", "question": "عدد نقاط تقاطع منحنى الدالة f(x) = -|x| + 2 مع محور السينات هو:", "options": ["2", "1", "0", "لا نهائي"], "answer": "2"},
    {"id": 127, "level": "متقدم", "question": "إذا كانت f(x) = x^2 - 2x، فإن فترة التناقص للدالة هي:", "options": ["(-مالا نهائية, 1]", "[1, مالا نهائية)", "ح", "[0, 2]"], "answer": "(-مالا نهائية, 1]"},
    {"id": 128, "level": "متقدم", "question": "إذا كانت f(x) = x^2 - 2x، فإن فترة التزايد للدالة هي:", "options": ["[1, مالا نهائية)", "(-مالا نهائية, 1]", "ح", "[2, مالا نهائية)"], "answer": "[1, مالا نهائية)"},
    {"id": 129, "level": "متقدم", "question": "مجال الدالة f(x) = جذر(x^2 - 3x + 2) هو:", "options": ["(-مالا نهائية, 1] اتحاد [2, مالا نهائية)", "[1, 2]", "ح - {1, 2}", "ح"], "answer": "(-مالا نهائية, 1] اتحاد [2, مالا نهائية)"},
    {"id": 130, "level": "متقدم", "question": "ما هو مدى الدالة f(x) = |x - 3| / (x - 3) + 2 هو:", "options": ["{1, 3}", "{0, 2}", "ح", "[1, 3]"], "answer": "{1, 3}"},
    {"id": 131, "level": "متقدم", "question": "إذا كانت f دالة زوجية وكان $\\int$ أو خصائص التماثل تحقق أن f(x) = f(-x)، فما قيمة f(2) - f(-2) إذا كانت f(2) = 7 ؟", "options": ["0", "14", "7", "-7"], "answer": "0"},
    {"id": 132, "level": "متقدم", "question": "مجال الدالة f(x) = 1 / جذر(6 + x - x^2) هو:", "options": ["(-2, 3)", "[-2, 3]", "ح - {-2, 3}", "(-مالا نهائية, -2) اتحاد (3, مالا نهائية)"], "answer": "(-2, 3)"},
    {"id": 133, "level": "متقدم", "question": "إذا كانت f(x) = x^3 - 3x، فإن نوع الدالة وتماثلها هو:", "options": ["فردية وتماثل حول نقطة الأصل", "زوجية وتماثل حول الصادات", "ليست زوجية ولا فردية", "ثابتة"], "answer": "فردية وتماثل حول نقطة الأصل"},
    {"id": 134, "level": "متقدم", "question": "منحنى الدالة f(x) = (x - 1)^3 + 2 يمر بنقطة التماثل:", "options": ["(1, 2)", "(-1, -2)", "(1, -2)", "(-1, 2)"], "answer": "(1, 2)"},
    {"id": 135, "level": "متقدم", "question": "إذا كانت f(x) = 3^x، فإن الدالة العكسية لها f^-1(x) تسمى:", "options": ["log_3(x)", "3x", "x^3", "1 / (3^x)"], "answer": "log_3(x)"},
    {"id": 136, "level": "متقدم", "question": "ما هو مجال الدالة f(x) = جذر(x^2) هو:", "options": ["ح", "[0, مالا نهائية)", "ح - {0}", "(0, مالا نهائية)"], "answer": "ح"},
    {"id": 137, "level": "متقدم", "question": "مدى الدالة f(x) = جذر(x^2) هو:", "options": ["[0, مالا نهائية)", "ح", "(-مالا نهائية, 0]", "ح - {0}"], "answer": "[0, مالا نهائية)"},
   {"id": 138, "level": "متقدم", "question": "إذا كانت f(x) = |x|، فإن متوسط التغير في الدالة على الفترة [-1, 2] يساوي:", "options": ["1/3", "1/2", "1", "2"], "answer": "1/3"},
    {"id": 139, "level": "متقدم", "question": "إذا كانت f(x) دالة معرفة بقاعدتين وكانت متصلة عند نقطة الفاصل a، فإن:", "options": ["النهاية اليمنى = النهاية اليسرى = قيمة الدالة", "النهاية اليمنى لا تساوي اليسرى", "الدالة غير قابلة للاشتقاق فقط", "لا توجد شروط"], "answer": "النهاية اليمنى = النهاية اليسرى = قيمة الدالة"},
    {"id": 140, "level": "متقدم", "question": "مجال الدالة f(x) = log(x^2 - 4) معتبرة كدالة حقيقية نطاقها الموجب الصريح للجذر أو اللوغاريتم هو:", "options": ["(-مالا نهائية, -2) اتحاد (2, مالا نهائية)", "(-2, 2)", "ح - {-2, 2}", "[-2, 2]"], "answer": "(-مالا نهائية, -2) اتحاد (2, مالا نهائية)"},
    {"id": 141, "level": "متقدم", "question": "إذا كانت f(x) = x / (x^2 + 1)، فما هي قيمة العظمى المطلقة للدالة؟", "options": ["1/2", "1", "0", "غير ذلك"], "answer": "1/2"},
    {"id": 142, "level": "متقدم", "question": "إذا كانت f(x) = -x / (x^2 + 1)، فما هي قيمة الصغرى المطلقة للدالة؟", "options": ["-1/2", "-1", "0", "1/2"], "answer": "-1/2"},
    {"id": 143, "level": "متقدم", "question": "ما هو مدى الدالة f(x) = x / |x| عندما x لا تساوي صفر:", "options": ["{-1, 1}", "ح", "[0, 1]", "[-1, 1]"], "answer": "{-1, 1}"},
    {"id": 144, "level": "متقدم", "question": "إذا كانت f(x) دالة فردية وكانت f(3) = -5، فإن f(-3) تساوي:", "options": ["5", "-5", "0", "3"], "answer": "5"},
    {"id": 145, "level": "متقدم", "question": "إذا كانت f(x) دالة زوجية وكانت f(4) = 7، فإن f(-4) تساوي:", "options": ["7", "-7", "0", "4"], "answer": "7"},
    {"id": 146, "level": "متقدم", "question": "مجال الدالة f(x) = جذر(x - 2) + 1 / جذر(5 - x) هو:", "options": ["[2, 5)", "[2, 5]", "(2, 5)", "ح - {5}"], "answer": "[2, 5)"},
    {"id": 147, "level": "متقدم", "question": "إذا كانت f(x) = (x - 2)^3 + 1، فإن الدالة العكسية f^-1(x) هي:", "options": ["الجذر التكعيبي لـ (x - 1) + 2", "الجذر التكعيبي لـ (x + 1) - 2", "x^3 + 2", "(x - 2) / 3"], "answer": "الجذر التكعيبي لـ (x - 1) + 2"},
    {"id": 148, "level": "متقدم", "question": "منحنى الدالة f(x) = -|x| انعكاس لمنحنى y = |x| في:", "options": ["محور السينات", "محور الصادات", "نقطة الأصل", "المستقيم y = x"], "answer": "محور السينات"},
    {"id": 149, "level": "متقدم", "question": "إذا كانت f(x) = 2^(x+1)، فإن f(x - 1) تساوي:", "options": ["2^x", "2^(x-1)", "2^(x+2)", "2 * 2^x"], "answer": "2^x"},
    {"id": 150, "level": "متقدم", "question": "التركيب (f o f)(x) إذا كانت f(x) = x + 1 هو:", "options": ["x + 2", "x^2 + 1", "2x + 1", "x + 1"], "answer": "x + 2"}
]

# ==========================================
# دالة اختبار وتنفيذ بنك الأسئلة بالكامل
# ==========================================
def run_full_quiz():
    print(f"تم تحميل بنك الأسئلة بنجاح! الإجمالي: {len(questions_db)} سؤالاً حقيقياً ومتنوعاً (50 لكل مستوى).\n")
    
    # عداد الأسئلة لكل مستوى للتأكد
    levels = {"مبتدئ": 0, "متوسط": 0, "محترف": 0}
    for q in questions_db:
        levels[q['level']] += 1
    
    print(f"توزيع الأسئلة الدقيق:")
    for lvl, count in levels.items():
        print(f"- مستوى ({lvl}): {count} سؤالاً")

if __name__ == "__main__":
    run_full_quiz()


@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = [q for q in questions_db if q.get('level') == level]
    if not pool:
        pool = [q for q in questions_db if q.get('level') == "متوسط"]
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "question": questions[current_index]['question'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": (ans == questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة</div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <p dir="auto"><strong>السؤال {{ current_num }}:</strong> <span dir="auto">{{ question.question }}</span></p>
        </div>

        <h2>اختبار الدرس الأول مادة الرياضيات البحتة</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
             <p dir="auto"><strong>السؤال {{ current_num }}:</strong> <span dir="auto">{{ question.question }}</span></p>
               
                <div class="options-list">
                    {% for opt in question.options %}
<label class="option-item" dir="auto">
    <input type="radio" name="current_answer" value="{{ opt }}" required> 
    <span dir="auto">{{ opt }}</span>
</label>
                    {% endfor %}
                </div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

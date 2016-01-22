#!/usr/bin/env python
# -*- coding: utf-8 -*--
"""Collection of all functions for the questionnaire."""
from collections import OrderedDict
from datetime import date
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .. import forms
from .. import models
from . import general


@login_required
def questionnaire_instructions(request):
    """Render the instructions page for the questionnaire."""
    current_user = request.user

    finished_parts = get_finished_parts(current_user)
    single_finished_parts = finished_parts["single_finished_parts"]
    all_parts_finished = finished_parts["all_parts_finished"]

    context = {
        "single_finished_parts": single_finished_parts,
        "all_parts_finished": all_parts_finished,
        "active_test": "active",
    }

    return render(request, "grpalloc/questionnaire_instructions.html", context)


def get_questionnaire_model(current_user):
    """Return the model of the current users Questionnaire DB."""
    try:
        points = models.Questionnaire.objects.get(usr=current_user)
    except ObjectDoesNotExist:
        # create Questionnaire entry for user
        models.Questionnaire.objects.create(usr=current_user)
        points = models.Questionnaire.objects.get(usr=current_user)

    return points


def get_value_of_forms():
    """Return a dict with the value '0' and the key 'pointsq*'; * = 1-7."""
    value_of_forms = {}
    for points in range(1, 8):
        value_of_forms["pointsq" + str(points)] = "0"
    return value_of_forms


def get_value_questionnaire_parts(part, current_user):
    """Get points from the questionnaire part and current user as dict."""
    # set initial value from all points to 0
    value_of_forms = get_value_of_forms()
    points = get_questionnaire_model(current_user)

    if part == "1":
        value_of_forms = {
            "pointsq1": points.p1q1,
            "pointsq2": points.p1q2,
            "pointsq3": points.p1q3,
            "pointsq4": points.p1q4,
            "pointsq5": points.p1q5,
            "pointsq6": points.p1q6,
            "pointsq7": points.p1q7,
            "pointsq8": points.p1q8,
        }
    elif part == "2":
        value_of_forms = {
            "pointsq1": points.p2q1,
            "pointsq2": points.p2q2,
            "pointsq3": points.p2q3,
            "pointsq4": points.p2q4,
            "pointsq5": points.p2q5,
            "pointsq6": points.p2q6,
            "pointsq7": points.p2q7,
            "pointsq8": points.p2q8,
        }
    elif part == "3":
        value_of_forms = {
            "pointsq1": points.p3q1,
            "pointsq2": points.p3q2,
            "pointsq3": points.p3q3,
            "pointsq4": points.p3q4,
            "pointsq5": points.p3q5,
            "pointsq6": points.p3q6,
            "pointsq7": points.p3q7,
            "pointsq8": points.p3q8,
        }
    elif part == "4":
        value_of_forms = {
            "pointsq1": points.p4q1,
            "pointsq2": points.p4q2,
            "pointsq3": points.p4q3,
            "pointsq4": points.p4q4,
            "pointsq5": points.p4q5,
            "pointsq6": points.p4q6,
            "pointsq7": points.p4q7,
            "pointsq8": points.p4q8,
        }
    elif part == "5":
        value_of_forms = {
            "pointsq1": points.p5q1,
            "pointsq2": points.p5q2,
            "pointsq3": points.p5q3,
            "pointsq4": points.p5q4,
            "pointsq5": points.p5q5,
            "pointsq6": points.p5q6,
            "pointsq7": points.p5q7,
            "pointsq8": points.p5q8,
        }
    elif part == "6":
        value_of_forms = {
            "pointsq1": points.p6q1,
            "pointsq2": points.p6q2,
            "pointsq3": points.p6q3,
            "pointsq4": points.p6q4,
            "pointsq5": points.p6q5,
            "pointsq6": points.p6q6,
            "pointsq7": points.p6q7,
            "pointsq8": points.p6q8,
        }
    elif part == "7":
        value_of_forms = {
            "pointsq1": points.p7q1,
            "pointsq2": points.p7q2,
            "pointsq3": points.p7q3,
            "pointsq4": points.p7q4,
            "pointsq5": points.p7q5,
            "pointsq6": points.p7q6,
            "pointsq7": points.p7q7,
            "pointsq8": points.p7q8,
        }

    return value_of_forms


def get_finished_parts(current_user):
    """Get the finished parts from the questionnaire as dict."""
    user = general.current_user_instance(current_user)
    try:
        # get index if user has solved the test
        entry = models.Questionnaire.objects.get(usr=user)
        single_finished_parts = {
            "1": entry.p1f,
            "2": entry.p2f,
            "3": entry.p3f,
            "4": entry.p4f,
            "5": entry.p5f,
            "6": entry.p6f,
            "7": entry.p7f,
        }
        apf = entry.apf

    except ObjectDoesNotExist:
        single_finished_parts = {}
        for part in range(1, 8):
            single_finished_parts[part] = False
        apf = False

    single_finished_parts_sorted = OrderedDict(
        sorted(single_finished_parts.items(), key=lambda t: t[0]))

    context = {
        "single_finished_parts": single_finished_parts_sorted,
        "all_parts_finished": apf,
    }

    return context


def finished_part(points):
    """Return a value (0,1,2) depending on the points."""
    # Define part_finished depending on the summary
    # of the points
    part_finished = 0
    if sum(points) == 10:
        part_finished = 2
    elif sum(points) > 0:
        part_finished = 1
    return part_finished


def check_if_all_parts_finished(questions_model):
    """Check if all parts are completed and return it."""
    list_apf = []
    for parts_finished in questions_model:
        list_apf.append(parts_finished.p1f)
        list_apf.append(parts_finished.p2f)
        list_apf.append(parts_finished.p3f)
        list_apf.append(parts_finished.p4f)
        list_apf.append(parts_finished.p5f)
        list_apf.append(parts_finished.p6f)
        list_apf.append(parts_finished.p7f)

    for index, entry in enumerate(list_apf):
        if entry == 1 or entry == 0:
            # get the first part which is not finished
            return str(index + 1)

    # if all parts are saved, save the last fields
    # in the db and set the last part to true
    return True


def update_points(questions_model, part, points):
    """Update points the user has put in."""
    part_finished = finished_part(points)

    # Set the column 'apf' (all parts finished)
    # to False, because changes were made
    questions_model.update(apf=False,)

    # Save the single points to the database depending to the part
    if part == "2":
        questions_model.update(
            p1q1=points[0],
            p1q2=points[1],
            p1q3=points[2],
            p1q4=points[3],
            p1q5=points[4],
            p1q6=points[5],
            p1q7=points[6],
            p1q8=points[7],
            p1f=part_finished,)
    elif part == "3":
        questions_model.update(
            p2q1=points[0],
            p2q2=points[1],
            p2q3=points[2],
            p2q4=points[3],
            p2q5=points[4],
            p2q6=points[5],
            p2q7=points[6],
            p2q8=points[7],
            p2f=part_finished,)
    elif part == "4":
        questions_model.update(
            p3q1=points[0],
            p3q2=points[1],
            p3q3=points[2],
            p3q4=points[3],
            p3q5=points[4],
            p3q6=points[5],
            p3q7=points[6],
            p3q8=points[7],
            p3f=part_finished,)
    elif part == "5":
        questions_model.update(
            p4q1=points[0],
            p4q2=points[1],
            p4q3=points[2],
            p4q4=points[3],
            p4q5=points[4],
            p4q6=points[5],
            p4q7=points[6],
            p4q8=points[7],
            p4f=part_finished,)
    elif part == "6":
        questions_model.update(
            p5q1=points[0],
            p5q2=points[1],
            p5q3=points[2],
            p5q4=points[3],
            p5q5=points[4],
            p5q6=points[5],
            p5q7=points[6],
            p5q8=points[7],
            p5f=part_finished,)
    elif part == "7":
        questions_model.update(
            p6q1=points[0],
            p6q2=points[1],
            p6q3=points[2],
            p6q4=points[3],
            p6q5=points[4],
            p6q6=points[5],
            p6q7=points[6],
            p6q8=points[7],
            p6f=part_finished,)
    elif part == "end":
        questions_model.update(
            p7q1=points[0],
            p7q2=points[1],
            p7q3=points[2],
            p7q4=points[3],
            p7q5=points[4],
            p7q6=points[5],
            p7q7=points[6],
            p7q8=points[7],
            p7f=part_finished,)

        return check_if_all_parts_finished(questions_model)


def get_current_part(part):
    """Get the current part as string."""
    if part == "end":
        part = "7"
    else:
        part = str(int(part) - 1)
    return part


@login_required
def questionnaire_parts(request, part):
    """
    Main function of the questionnaire.

    Render the questions depending on the part and save the points.
    """
    available_parts = ["1", "2", "3", "4", "5", "6", "7", "end"]
    if part in available_parts:

        current_user = request.user

        # Load forms
        if request.method == 'POST':
            form = forms.QuestionnaireForm(request.POST)

            if form.is_valid():

                # points from the forms of the current part as int
                points = []
                points.append(int(form.cleaned_data["pointsq1"]))
                points.append(int(form.cleaned_data["pointsq2"]))
                points.append(int(form.cleaned_data["pointsq3"]))
                points.append(int(form.cleaned_data["pointsq4"]))
                points.append(int(form.cleaned_data["pointsq5"]))
                points.append(int(form.cleaned_data["pointsq6"]))
                points.append(int(form.cleaned_data["pointsq7"]))
                points.append(int(form.cleaned_data["pointsq8"]))

                # You don't have to check each single point
                # if it is in the range of 0-10 because it can't
                # be below 0 or above 10 from the radio buttons itself

                # Check whether 10 points are selected or not
                if sum(points) > 10:
                    messages.warning(request, "Zu viele Punkte"
                                     " verteilt! Maximal 10 Punkte möglich.")

                    # subract one part to render the
                    # same page again with the error
                    part = get_current_part(part)

                    return HttpResponseRedirect(reverse(
                        "questionnaire_parts", kwargs={'part': part}))

                # if points < 10 (0-10)
                else:
                    # get the User instance
                    user = general.current_user_instance(current_user)

                    try:
                        # try to get the model if entry exists
                        questions_model = models.Questionnaire.objects.filter(
                            usr=user)
                    except ObjectDoesNotExist:
                        # create Questionnaire entry for usr
                        models.Questionnaire.objects.create(usr=user)
                        questions_model = models.Questionnaire.objects.filter(
                            usr=user)

                    # apf is true if all parts are finished or it has the index
                    # of the not finished part
                    apf = update_points(questions_model, part, points)

                    if apf is True:
                        questions_model.update(
                            apf=apf,
                            date_test_finished=date.today(),)
                        # successfully exit the questionnaire
                        return HttpResponseRedirect(reverse("profile"))

                    # else jump to the (first) not finished part
                    elif apf is None:
                        # Go to the next part
                        return HttpResponseRedirect(reverse(
                            "questionnaire_parts",
                            kwargs={'part': part}))
                    else:
                        messages.info(
                            request, "Bitte zuerst alle Teile "
                                     "vervollständigen")
                        return HttpResponseRedirect(reverse(
                            "questionnaire_parts",
                            kwargs={'part': apf}))
            else:
                messages.warning(request, "Eingabefelder nicht gültig, "
                                 "bitte noch einmal probieren.")

        # if method != POST and the page just gets rendered
        else:
            # set initial value of forms if a test was already solved
            value_of_forms = get_value_questionnaire_parts(
                part, current_user)
            # load forms
            form = forms.QuestionnaireForm(initial=value_of_forms)

        # get the questions and headers from this function
        # and retrieve it as a dict in the "questions" variable
        questions = update_questionnaire_parts(part)

        finished_parts = get_finished_parts(current_user)
        # all arguments that are passed by rendering
        # the grpalloc/questionnaire_parts.html
        args = {
            "q_part": part,
            "questions": questions,
            "single_finished_parts": finished_parts["single_finished_parts"],
            "all_parts_finished": finished_parts["all_parts_finished"],
            "active_test": "active",
            "form": form, }
        # by rendering the html pass all the headers, questions
        # and more variables from update_questionnaire_parts(part)
        return render(request, "grpalloc/questionnaire_parts.html", args)

    raise Http404("Keine gültige Eingabe")


# pylint: disable=too-many-statements
def update_questionnaire_parts(q_part):
    """Give the questionnaire_parts the questions, header and more."""
    # q_part is the selected part (1 till 7) of the questionnaire as string (!)
    # passed through questionnaire_parts(request, part)
    q_part_width = int(q_part) * 14.3
    # q_part_width is the width of the progress bar
    # of the questionnaire_parts.html
    primary_header = "Fragebogen - Teil "
    # the primary_header is the h1 of the questionnaire_parts.html
    # - the part itself is loaded in the html-file via {{q_part}}

    # depending on which part is selected the sub_header
    # and the 8 questions are loaded dynamically
    if q_part == "1":
        sub_header = "Mein Beitrag zur Arbeitsgruppe"
        question1 = "Ich glaube, eine gute Gelegenheit schnell erkennen und "\
            "daraus Gewinn ziehen zu können."
        question2 = "Ich kann mit den verschiedensten Menschen gut "\
            "zusammenarbeiten."
        question3 = "Ich entwickle mit Leichtigkeit neue Ideen."
        question4 = "Merke ich, dass ein Gruppenmitglied etwas anzubieten hat"\
            ", bringe ich es dazu, es auszudrücken, so dass die "\
            "Gruppe davon profitiert."
        question5 = "Meine Fähigkeit, Problemen auf den Grund zu gehen, "\
            "ist meine Stärke."
        question6 = "Wenn dies zum Ziel führt, bin ich bereit, mich ab "\
            "und zu unbeliebt zu machen."
        question7 = "In einer mir vertrauten Situation merke ich schnell, "\
            "was Erfolg verspricht."
        question8 = "Ich kann Alternativen vorschlagen, ohne tendenziös zu "\
            "sein oder Vorurteile zu haben."
    elif q_part == "2":
        sub_header = "Meine Schwäche in der Gruppenarbeit ist vielleicht"
        question1 = "Ich fühle mich unwohl in unstrukturierten Diskussionen, "\
            "die in alle Richtungen verlaufen."
        question2 = "Ich bin zu nachgiebig gegenüber denen, die einen "\
            "brauchbaren Standpunkt vertreten, aber in der Gruppe wenig"\
            " Beachtung finden"
        question3 = "Wenn die Gruppe neue Ideen erarbeitet, neige ich dazu,"\
            " durch zu viel Sprechen sie nicht zu Wort kommen zu lassen."
        question4 = "Meine objektive Einstellung hindert mich daran, die "\
            "Begeisterung meiner Kollegen zu teilen."
        question5 = "Ich erscheine manchmal energisch und autoritär, wenn es "\
            "darum geht, Ergebnisse zu erzielen."
        question6 = "Ich habe Mühe, die Führungsposition zu übernehmen, weil "\
            "ich leicht von der Atmosphäre in der Gruppe beeinflusst werde."
        question7 = "Ich neige dazu, mich in den eigenen Gedanken zu "\
            "verlieren und nicht mehr denen der anderen zu folgen."
        question8 = "Meine Kollegen finden, dass ich mich zu viel mit Details"\
            " und Dingen beschäftige, die schlecht ausgehen könnten."
    elif q_part == "3":
        sub_header = "Meine Zusammenarbeit mit anderen im Rahmen "\
            "eines Projektes"
        question1 = "Ich schaffe es, die Kollegen zu beeinflussen, ohne sie "\
            "unter Druck zu setzen."
        question2 = "Meine Wachsamkeit hindert sie daran, "\
            "Unaufmerksamkeitsfehler oder Fehler aus Versehen zu begehen."
        question3 = "Ich bin bereit, vorwärts zu stoßen und wache darüber, "\
            "dass keine Zeit verloren geht und dass man vom Thema nicht "\
            "abweicht."
        question4 = "Man kann auf mich zählen für einen originellen Beitrag."
        question5 = "Für das gemeinsame Interesse bin ich immer bereit, einen"\
            " guten Vorschlag zu unterstützen."
        question6 = "Ich interessiere mich sehr für neue Ideen und für die "\
            "letzten Entwicklungen."
        question7 = "Ich glaube, dass meine Fähigkeit zur objektiven "\
            "Beurteilung von meinen Kollegen geschätzt wird."
        question8 = "Man kann sich auf mich verlassen, dass alles gut "\
            "organisiert ist."
    elif q_part == "4":
        sub_header = "Meine Art, an Gruppenarbeiten heranzutreten"
        question1 = "Ich interessiere mich dafür, meine Kollegen besser "\
            "kennen zu lernen."
        question2 = "Ich befürchte nicht, mich gegen die Ideen eines "\
            "Gruppenmitglieds zu stellen oder die Ansicht einer Minderheit "\
            "zu verteidigen."
        question3 = "Ich finde meistens Argumente, um eine falsche Meinung "\
            "zu widerlegen."
        question4 = "Ich glaube, Talent zu haben, die von der Gruppe "\
            "festgelegten Pläne in Taten umsetzen zu können."
        question5 = "Ich tendiere dazu, banale Lösungswege zu meiden, indem "\
            "ich Vorschläge bringe, die für die anderen überraschend sind."
        question6 = "Ich versehe all meine Unternehmungen mit einem Hauch "\
            "von Perfektionismus."
        question7 = "Ich bin bereit, außerhalb der Gruppe Kontakte "\
            "aufzunehmen und Auskünfte einzuholen."
        question8 = "Obwohl ich daran interessiert bin, mir den Standpunkt "\
            "aller anzuhören, habe ich keine Mühe, mich festzulegen, um "\
            "einen Entscheid zu fällen."
    elif q_part == "5":
        sub_header = "Warum ich Freude an der Arbeit habe"
        question1 = "Ich analysiere gerne diverse Situationen und wäge gerne "\
            "verschiedene Alternativen ab."
        question2 = "Ich finde gerne praktische Lösungen zu gestellten "\
            "Problemen."
        question3 = "Ich schätze das Gefühl, zu einem guten Arbeitsklima "\
            "beizutragen."
        question4 = "Ich kann einen starken Einfluss auf gewisse "\
            "Entscheidungen ausüben."
        question5 = "Ich begegne mit Offenheit Leuten, die neue Ideen "\
            "anzubieten haben."
        question6 = "Ich bin in der Lage, Leute zu einem Konsens über die "\
            "durchzuführenden Handlungen zu bringen."
        question7 = "Ich fühle mich in meinem Element, wenn ich mich ganz auf"\
            " eine Aufgabe konzentrieren kann."
        question8 = "Ich behandle gerne Situationen, die meine Phantasie "\
            "herausfordern."
    elif q_part == "6":
        sub_header = "Wäre ich plötzlich mit einer schwierigen Aufgabe "\
            "konfrontiert, die ich innert einer beschränkten Zeit und "\
            "mit mir unbekannten Leuten erledigen soll"
        question1 = "Ich würde mich gerne in eine Ecke zurückziehen, um eine "\
            "Lösung zu entwickeln, die es erlauben würde, aus der "\
            "Sackgasse zu kommen."
        question2 = "Ich würde es vorziehen, mit der Person zu arbeiten, die "\
            "die besten Ideen hat - auch wenn sie mühsam ist."
        question3 = "Ich würde die Schwierigkeiten zu verringern versuchen, "\
            "indem ich bestimmen würde, wie jeder am besten seinen Beitrag "\
            "leistet."
        question4 = "Meine Fähigkeit, Prioritäten zu setzen, würde dazu "\
            "beitragen, dass die Gruppe die Termine einhält."
        question5 = "Ich meine, ich würde den Kopf nicht verlieren und "\
            "weiterhin logisch denken."
        question6 = "Ich würde - trotz Druck - die Ziele nicht aus den Augen "\
            "verlieren."
        question7 = "Ich wäre bereit, einen ersten Schritt zu machen, wenn "\
            "ich sehen würde, dass die Gruppe keinen Fortschritt erzielt."
        question8 = "Ich würde die Diskussion mit dem Ziel eröffnen, neue "\
            "Ideen zu fördern und Bewegung in Gang zu bringen."
    elif q_part == "7":
        sub_header = "Die Probleme, denen ich bei der Gruppenarbeit "\
            "unterworfen bin"
        question1 = "Ich bin manchmal ungeduldig mit denen, die den Weg"\
            " blockieren."
        question2 = "Man wirft mir manchmal vor, zu analytisch und zu"\
            " wenig intuitiv zu sein."
        question3 = "Mein Wunsch die Arbeit perfekt zu machen, kann das "\
            "Fortschreiten verlangsamen."
        question4 = "Ich neige dazu, mich sehr schnell zu langweilen und"\
            " drehe mich dann zu nur einem oder zwei Kollegen um, von denen"\
            " ich weiß, dass sie mich stimulieren können"
        question5 = "Ich habe Mühe anzulaufen, bevor die Ziele genau klar"\
            " sind."
        question6 = "Ich habe manchmal Mühe, die schwierigen Punkte, die ich "\
            "aufgeworfen habe, zu erläutern und zu klären."
        question7 = "Ich bin mir bewusst, dass ich von Anderen Dinge verlange"\
            ", die ich selber nicht tun kann."
        question8 = "Ich zögere, Meinungen auszudrücken, von denen ich weiß,"\
            " dass sie auf eine starke Opposition stoßen werden."
    else:
        # just in case of an error-template, it shouldn't be possible that this
        # gets ever triggered because of the if / else statement in
        # questionnaire_parts which only allows the seven strings 1 - 7
        primary_header = "Fragebogen - Error"
        sub_header = "Bitte erneut laden"

    # set the value (button_value) and the parameter (next_part)
    # to the button depending on which part of the test (7 or not 7)
    if q_part != "7":
        next_part = int(q_part) + 1
        button_value = "Weiter"
    elif q_part == "7":
        next_part = "end"
        button_value = "Persönlichkeitstest abschließen"

    arguments = {
        "primary_header": primary_header,
        "sub_header": sub_header,
        "q_part_width": q_part_width,
        "q_part": q_part,
        "next_q_part": str(next_part),
        "button_value": button_value,
        "q1": question1,
        "q2": question2,
        "q3": question3,
        "q4": question4,
        "q5": question5,
        "q6": question6,
        "q7": question7,
        "q8": question8,
    }

    return arguments

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


def plotReconstructionManual(self):
    """
    Funkcja umożliwia wyświetlenie interaktywnego wykresu umożliwiającego manualną rekonstrukcję
    twarzy używając twarzy własnych i pierwszych dziewięciu wag. Do kontroli wag używane są suwaki.
    Przyciskk 'Reset' resetuje cały wykres do stanu początkowego.
    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
        Przekazany aby móc osadzić wykresy w GUI oraz aby uzyskać dane do wizualizacji.
    """
    figure = create_plots(self, self.VisualizationReconstructionTab)
    ax1 = figure.add_subplot(121)
    ax2 = figure.add_subplot(122)
    plt.subplots_adjust(right=0.65)
    ax1.imshow(self.fr.mean_img, cmap=plt.cm.gray)
    plt.axis('off')
    fig_title = 'Manualna rekonstrukcja twarzy na podstawie wag i twarzy własnych.'
    plt.text(1.5, 1.45, fig_title,
             horizontalalignment='center',
             fontsize=14,
             transform=ax1.transAxes)

    ax1_e = plt.axes([0.77, 0.7, 0.15, 0.03])
    ax2_e = plt.axes([0.77, 0.65, 0.15, 0.03])
    ax3_e = plt.axes([0.77, 0.6, 0.15, 0.03])
    ax4_e = plt.axes([0.77, 0.55, 0.15, 0.03])
    ax5_e = plt.axes([0.77, 0.5, 0.15, 0.03])
    ax6_e = plt.axes([0.77, 0.45, 0.15, 0.03])
    ax7_e = plt.axes([0.77, 0.4, 0.15, 0.03])
    ax8_e = plt.axes([0.77, 0.35, 0.15, 0.03])
    ax9_e = plt.axes([0.77, 0.3, 0.15, 0.03])

    # mean face to weights
    mean_face_9pca = np.matmul(
        self.fr.face_weights[0], self.fr.eigenfaces.reshape(np.shape(self.fr.eigenfaces)[0], 86 * 86))[:9]

    # Back
    reconstructed_face_template = self.fr.mean_img
    for iter, eigenface in enumerate(self.fr.eigenfaces[:9]):
        reconstructed_face_template += np.dot(mean_face_9pca[iter], eigenface)
    ax2.imshow(reconstructed_face_template, cmap=plt.cm.gray)
    plt.axis('off')

    slider_1 = Slider(ax1_e, 'waga 1', -5000, 5000, valinit=mean_face_9pca[0], valfmt="%.0f")
    slider_2 = Slider(ax2_e, 'waga 2', -5000, 5000, valinit=mean_face_9pca[1], valfmt="%.0f")
    slider_3 = Slider(ax3_e, 'waga 3', -5000, 5000, valinit=mean_face_9pca[2], valfmt="%.0f")
    slider_4 = Slider(ax4_e, 'waga 4', -5000, 5000, valinit=mean_face_9pca[3], valfmt="%.0f")
    slider_5 = Slider(ax5_e, 'waga 5', -5000, 5000, valinit=mean_face_9pca[4], valfmt="%.0f")
    slider_6 = Slider(ax6_e, 'waga 6', -5000, 5000, valinit=mean_face_9pca[5], valfmt="%.0f")
    slider_7 = Slider(ax7_e, 'waga 7', -5000, 5000, valinit=mean_face_9pca[6], valfmt="%.0f")
    slider_8 = Slider(ax8_e, 'waga 8', -5000, 5000, valinit=mean_face_9pca[7], valfmt="%.0f")
    slider_9 = Slider(ax9_e, 'waga 9', -5000, 5000, valinit=mean_face_9pca[8], valfmt="%.0f")

    def update(val):
        mean_face_9pca = [slider_1.val, slider_2.val, slider_3.val, slider_4.val,
                          slider_5.val, slider_6.val, slider_7.val, slider_8.val,
                          slider_9.val]

        reconstructed_face = np.copy(self.fr.mean_img)
        for iter, eigenface in enumerate(self.fr.eigenfaces[:9]):
            reconstructed_face += np.dot(mean_face_9pca[iter], eigenface)

        ax2.imshow(reconstructed_face, cmap=plt.cm.gray)

    slider_1.on_changed(update)
    slider_2.on_changed(update)
    slider_3.on_changed(update)
    slider_4.on_changed(update)
    slider_5.on_changed(update)
    slider_6.on_changed(update)
    slider_7.on_changed(update)
    slider_8.on_changed(update)
    slider_9.on_changed(update)

    def reset(event):
        slider_1.reset();
        slider_2.reset();
        slider_3.reset();
        slider_4.reset();
        slider_5.reset();
        slider_6.reset();
        slider_7.reset();
        slider_8.reset();
        slider_9.reset();
        ax2.imshow(reconstructed_face_template, cmap=plt.cm.gray)

    resetax = plt.axes([0.45, 0.05, 0.1, 0.1])
    self._rec_man_button = Button(resetax, 'Reset', hovercolor='0.8')
    self._rec_man_button.on_clicked(reset)


def plotTSNE(self):
    """
    Funkcja wyświetla wyniki obliczone metodą t-SNE wizualizującą dane z przestrzeni wielowymiarowej
    do przestrzeni o mniejszej wymiarowości.

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
        Przekazany aby móc osadzić wykresy w GUI oraz uzyskać obliczone z t-SNE dane.
    """
    figure = create_plots(self, self.VisualizationTSNETab)
    ax = figure.add_subplot(111)
    plt.title('TSNE plot')
    ax.scatter(self.fr.t_sne[:, 0], self.fr.t_sne[:, 1])

    # Zdjęcia do wyświetlenia to oryginalne - nieprzetworzone zdjęcia twarzy
    images_to_plot = np.array(np.transpose(self.fr.image_matrix_raw)) \
        .reshape(self.fr.image_count, self.fr.image_shape, self.fr.image_shape)

    for id, coord in enumerate(np.array(self.fr.t_sne)):
        ab = AnnotationBbox(
            OffsetImage(images_to_plot[id], zoom=0.3, cmap=plt.cm.gray),
            coord,
            pad=0,
            xybox=(0., 0.),
            boxcoords="offset points")
        ax.add_artist(ab)
    ax.set_title('Rzutowanie danych do reprezentacji 2D z użyciem TSNE')


def plotPCA2components(self):
    """
    Funkcja wizualizująca twarze dodane do bazy danych przedstawione w 2D na podstawie obliczonych
    dla nich dwóch pierwszych składowych głównych z PCA.

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
        Przekazany aby móc osadzić wykresy w GUI oraz zaprezentować rozkład twarzy na podstawie
        wartości twarzy z dwóch pierwszych składowych głównych.
    """
    # Zamknij wcześniej stworzone wykresy
    plt.close('all')
    # Stwórz nową figurę
    figure = create_plots(self, self.Visualization2PCATab)
    face_weights_plot = np.matmul(self.fr.image_matrix_flat.transpose(),
                                  self.fr.eigenfaces_flat[:2].transpose()).transpose()
    ax = figure.add_subplot(111)
    images_to_plot = np.array(np.transpose(self.fr.image_matrix_raw)) \
        .reshape(self.fr.image_count, self.fr.image_shape, self.fr.image_shape)

    for id, coord in enumerate(np.array(face_weights_plot.T)):
        ab = AnnotationBbox(
            OffsetImage(images_to_plot[id], zoom=0.3, cmap=plt.cm.gray),
            coord,
            pad=0,
            xybox=(0., 0.),
            boxcoords="offset points")
        ax.add_artist(ab)

    ax.grid(True)
    ax.set_xlim([np.min(self.fr.face_weights[:, 0]) * 1.2, np.max(self.fr.face_weights[:, 0]) * 1.2])
    ax.set_ylim([np.min(self.fr.face_weights[:, 1]) * 1.2, np.max(self.fr.face_weights[:, 1]) * 1.2])
    ax.set_xlabel('Pierwsza składowa główna')
    ax.set_ylabel('Druga składowa główna')
    ax.set_title('Wizualizacja danych z użyciem dwóch pierwszych składowych głównych')


def plotEigenfaces(self):
    """Funkcja wizualizująca obliczone twarze własne. Pierwszych dziewięć twarzy własnych jest
    zaprezentowanych na figurze.

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
              Przekazany aby móc osadzić wykresy w GUI oraz zaprezentować obliczone twarze własne.
    """
    figure = create_plots(self, self.VisualizationEigenfacesTab, toolbar=False)
    rows = 3
    cols = 3
    eigenface_titles = ["Twarz własna %d" % i for i in range(1, self.fr.eigenfaces.shape[0] + 1)]
    figure.subplots_adjust(bottom=0.1, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(rows * cols):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(self.fr.eigenfaces[i], cmap=plt.cm.gray)
        plt.title(eigenface_titles[i], size=12)
        plt.xticks(())
        plt.yticks(())
    figure.suptitle('Pierwsze {} twarzy własnych'.format(rows * cols), fontsize=14)


def plotPCAcomponents(self):
    """
    Funkcja wizualizująca składowe główne obliczone metodą PCA przy obliczaniu twarzy własnych.
    Oś x: kolejne składowe główne
    Oś y: procent wariancji reprezentowanej przez składową

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
        Przekazany aby móc osadzić wykresy w GUI oraz zaprezentować procent wariancji
        reprezentowany przez składowe.
    """
    figure = create_plots(self, self.VisualizationPCACoeffTab)
    ax = figure.add_subplot(111)
    X = list(range(1, self.fr.eigenfaces_n + 1))
    ax.bar(X, self.fr.explained_variance_ratio_)
    ax.set_xlabel('N-ty główny komponent')
    ax.set_ylabel('Wartosc procentowa reprezentowanej wariancji')
    ax.set_title('Procentowa reprezentacja wariancji dla poszczególnych głównych składowych')


def create_plots(self, parent, toolbar=True):
    """
    Funkcja tworząca figurę osadzoną w GUI przekazanym w argumencie *self* w elemencie *parent*.

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.
              Przekazany aby móc osadzić wykresy w GUI.

        parent: Zawiera QWidget w którym zaprezentowana ma być figura.

        toolbar: Argument opcjonalny. *True* - wyświetl pasek narzędzi. *False* - nie wyświetlaj.

    Returns:
        figure: Zostaje zwrócona figura na której można osadzić wykres.
    """
    figure = plt.figure(figsize=(9.2, 5.8))
    figure.subplots_adjust(top=.85)
    canvas = FigureCanvas(figure)
    canvas.setParent(parent)
    if toolbar:
        toolbar = NavigationToolbar(canvas, self)
        toolbar.setParent(parent)
    figure.clear()
    return figure

def create_messagebox(self, wintitle, text):
    """
    Funkcja tworzy i wyświetla okno informacyjne blokujące aplikację GUI aż do zamkniecia okna.

    Args:
        self: Obiekt GUI kontrolujący aplikację wraz ze wszystkimi obliczonymi w aplikacji danymi.

        wintitle: Informacja do wyświetlenia w tytule okna.

        text: Informacja do wyświetlenia w oknie informacji.
    """
    self.msg = QMessageBox()
    self.msg.setIcon(QMessageBox.Information)
    self.msg.setWindowIcon(QIcon('app_icon.jpg'))
    self.msg.setWindowTitle(wintitle)
    self.msg.setText(text)
    self.msg.exec_()

def show_found_face(image_s, data, cnn=False, id=-1):
    """
    Funkcja wyświetla w oddzielnym od aplikacji GUI oknie twarz przekazaną w argumentach w celu
    porównania szukanej i znalezionej twarzy.

    Args:
        image_s: Szukana twarz w skali szarości bądź RGB.

        data: Zależna od wartości cnn.

        Gdy *cnn* = True -  przekazywane są dwa parametry:
        1. Szukane zdjęcie.
        2. Lista o trzech elementach zawierająca prawdopodobieństwa przynależności do danej klasy,
        baza danych z nieprzetworzonymi zdjęciami twarzy, etykiety do bazy danych zdjęć, umożliwiające
        połączenie prawdopodobieństw przynależności do zdjęć w bazie.
        Gdy *cnn* = False - Jedynie szukane zdjęcie.

        cnn: Argument opcjonalny determinujący czy zdjęcia ma być szukane z użyciem danych z sieci
        neuronowej, czy wyświetlone ma być znalezione zdjęcie dla twarzy własnych.
    """
    # Zablokuj wyskakujące okna wcześniejszych wykresów
    plt.close('all')

    if cnn:
        # Rozpakuj przekazane dane
        candidates = len(data[0])
        candidates_id = np.argsort(-data[0])
        candidates_proba = sorted([round(100 * x, 1) for x in data[0]], reverse=True)
        image_database = data[1]
        labels = data[2]

        fig = plt.figure(figsize=(11, 5))
        fig.suptitle("Wyświetlenie najbardziej podobnej osoby", fontsize=20)

        # Definicja wykresów
        searched_ax = plt.subplot2grid((3, 7 if candidates else 6), (0, 0), colspan=3, rowspan=3)
        searched_ax.set_title("Poszukiwana osoba")
        searched_ax.imshow(image_s, cmap='gray')
        plt.xticks([])
        plt.yticks([])

        found_ax = plt.subplot2grid((3, 7 if candidates else 6), (0, 3), colspan=3, rowspan=3)
        found_ax.set_title("Znaleziona osoba")
        found_ax.imshow(image_database[np.where(np.array(labels) == candidates_id[0])[0][3]], cmap='gray')
        found_ax.text(0.95, 0.05, 'ID osoby: {}'.format(candidates_id[0]),
                      verticalalignment='bottom', horizontalalignment='right',
                      transform=found_ax.transAxes,
                      color='red', fontsize=10)
        found_ax.text(0.95, 0, 'Podobieństwo: {}%'.format(candidates_proba[0]),
                      verticalalignment='bottom', horizontalalignment='right',
                      transform=found_ax.transAxes,
                      color='red', fontsize=10)

        plt.xticks([])
        plt.yticks([])

        similar1_ax = plt.subplot2grid((3, 7), (0, 6))
        similar1_ax.set_title("Podobne osoby", fontdict={'size': 10})
        similar1_ax.imshow(image_database[np.where(np.array(labels) == candidates_id[1])[0][3]], cmap='gray')
        plt.xticks([])
        plt.yticks([])
        similar1_ax.text(0.95, 0, 'ID osoby: {}'.format(candidates_id[1]),
                      verticalalignment='bottom', horizontalalignment='right',
                      transform=similar1_ax.transAxes,
                      color='red', fontsize=10)
        similar1_ax.text(0.95, 0.12, '{}%'.format(candidates_proba[1]),
                         verticalalignment='bottom', horizontalalignment='right',
                         transform=similar1_ax.transAxes,
                         color='red', fontsize=10)

        # Zależnie od ilości kandydatów wyświetl do 3 dodatkowych zdjęć z wartościami procentowymi
        if candidates > 2:
            similar2_ax = plt.subplot2grid((3, 7), (1, 6))
            plt.xticks([])
            plt.yticks([])
            similar2_ax.imshow(image_database[np.where(np.array(labels) == candidates_id[2])[0][3]], cmap='gray')
            similar2_ax.text(0.95, 0, 'ID osoby: {}'.format(candidates_id[2]),
                             verticalalignment='bottom', horizontalalignment='right',
                             transform=similar2_ax.transAxes,
                             color='red', fontsize=10)
            similar2_ax.text(0.95, 0.12, '{}%'.format(candidates_proba[2]),
                             verticalalignment='bottom', horizontalalignment='right',
                             transform=similar2_ax.transAxes,
                             color='red', fontsize=10)

            if candidates > 3:
                similar3_ax = plt.subplot2grid((3, 7), (2, 6))
                plt.xticks([])
                plt.yticks([])
                similar3_ax.imshow(image_database[np.where(np.array(labels) == candidates_id[3])[0][3]], cmap='gray')
                similar3_ax.text(0.95, 0, 'ID osoby: {}'.format(candidates_id[3]),
                                 verticalalignment='bottom', horizontalalignment='right',
                                 transform=similar3_ax.transAxes,
                                 color='red', fontsize=10)
                similar3_ax.text(0.95, 0.12, '{}%'.format(candidates_proba[3]),
                                 verticalalignment='bottom', horizontalalignment='right',
                                 transform=similar3_ax.transAxes,
                                 color='red', fontsize=10)

    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        fig.suptitle("Wyświetlenie najbardziej podobnej osoby", fontsize=20)

        ax1.set_title("Poszukiwana osoba")
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])

        ax2.set_title("Znaleziona osoba")
        ax2.set_yticklabels([])
        ax2.set_xticklabels([])

        if id >= 0:
            ax2.text(0.9, 0.05, 'ID: {}'.format(id),
                     verticalalignment='bottom', horizontalalignment='right',
                     transform=ax2.transAxes,
                     color='red', fontsize=13)

        ax1.imshow(image_s, cmap='gray')
        ax2.imshow(data, cmap='gray')


    plt.show()
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj): #Bu fonksiyon her obje (örneğin bir UserProfile) için çağrılır. “Bu kullanıcının bu objeye erişme hakkı var mı?”
        """Check user is trying to edit their own profile"""

        if request.method in permissions.SAFE_METHODS: #get gibi safe bir method ise izin verilecek, diğer kullanıcılara. Yani bakabilirler emailine adına ama bir put patch delete yapamazlar, - `GET`, `HEAD`, `OPTIONS` gibi **zararsız (SAFE)** metodlar için **izin ver**  
            return True
        
        return obj.id == request.user.id #bir boolen dönecek. Eğer safe bir method kullanmıyorsa bakıcaz bu kendi hesabı mı diye
